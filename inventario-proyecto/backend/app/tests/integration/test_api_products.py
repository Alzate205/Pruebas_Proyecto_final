import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db


@pytest.fixture(scope="function")
def test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


client = TestClient(app)


def test_create_product_api(test_db):
    cat_response = client.post("/api/categories/", json={"name": "Electrónica"})
    category_id = cat_response.json()["id"]
    
    response = client.post("/api/products/", json={
        "name": "Laptop",
        "description": "Laptop HP",
        "price": 500.0,
        "stock": 10,
        "category_id": category_id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Laptop"


def test_list_products_api(test_db):
    cat_response = client.post("/api/categories/", json={"name": "Hogar"})
    category_id = cat_response.json()["id"]
    
    client.post("/api/products/", json={
        "name": "Mesa",
        "description": "Mesa de madera",
        "price": 150.0,
        "stock": 5,
        "category_id": category_id
    })
    
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(p["name"] == "Mesa" for p in data)