from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_music():
    response = client.post("/music/", json={"name": "Test Music", "description": "A music for testing"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Music"

def test_read_music():
    response = client.post("/music/", json={"name": "Test Music", "description": "A music for testing"})
    item_id = response.json()["id"]
    response = client.get(f"/music/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Music"

def test_update_music():
    response = client.post("/music/", json={"name": "Test Music", "description": "A music for testing"})
    item_id = response.json()["id"]
    response = client.put(f"/music/{item_id}", json={"name": "Updated Music", "description": "Updated description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Music"

def test_delete_music():
    response = client.post("/music/", json={"name": "Test Music", "description": "A music for testing"})
    item_id = response.json()["id"]
    response = client.delete(f"/music/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Music"
