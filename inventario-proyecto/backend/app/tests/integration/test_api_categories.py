from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_category_api():
    response = client.post("/api/categories/", json={"name": "Ropa"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Ropa"


def test_list_categories_api():
    # Nos aseguramos de que al menos exista una
    client.post("/api/categories/", json={"name": "Calzado"})
    response = client.get("/api/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(c["name"] == "Calzado" for c in data)
