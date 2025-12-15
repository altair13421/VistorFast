from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_anilist():
    response = client.post("/anilist/", json={"name": "Test Anilist", "description": "A anilist for testing"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Anilist"

def test_read_anilist():
    response = client.post("/anilist/", json={"name": "Test Anilist", "description": "A anilist for testing"})
    item_id = response.json()["id"]
    response = client.get(f"/anilist/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Anilist"

def test_update_anilist():
    response = client.post("/anilist/", json={"name": "Test Anilist", "description": "A anilist for testing"})
    item_id = response.json()["id"]
    response = client.put(f"/anilist/{item_id}", json={"name": "Updated Anilist", "description": "Updated description"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Anilist"

def test_delete_anilist():
    response = client.post("/anilist/", json={"name": "Test Anilist", "description": "A anilist for testing"})
    item_id = response.json()["id"]
    response = client.delete(f"/anilist/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Anilist"
