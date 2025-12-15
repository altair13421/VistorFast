from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_nyaa():
    response = client.post("/nyaa/", json={"name": "Test Nyaa", "description": "A nyaa for testing"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Nyaa"

def test_read_nyaa():
    response = client.post("/nyaa/", json={"name": "Test Nyaa", "description": "A nyaa for testing"})
    item_id = response.json()["id"]
    response = client.get(f"/nyaa/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Nyaa"

def test_update_nyaa():
    response = client.post("/nyaa/", json={"name": "Test Nyaa", "description": "A nyaa for testing"})
    item_id = response.json()["id"]
    response = client.put(f"/nyaa/{item_id}", json={"name": "Updated Nyaa", "description": "Updated description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Nyaa"

def test_delete_nyaa():
    response = client.post("/nyaa/", json={"name": "Test Nyaa", "description": "A nyaa for testing"})
    item_id = response.json()["id"]
    response = client.delete(f"/nyaa/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Nyaa"
