from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_product_api():
    # Primero crear categoría
    cat_response = client.post("/api/categories/", json={"name": "Electrónica"})
    category_id = cat_response.json()["id"]
    
    # Crear producto
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


def test_list_products_api():
    # Crear categoría y producto
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