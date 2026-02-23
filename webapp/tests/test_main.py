import pytest
from fastapi.testclient import TestClient
from webapp.main import app

client = TestClient(app)


def test_generate_defaults():
    response = client.post("/generate", json={})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 20
    assert data["total"] == 20
    assert data["page"] == 1
    assert data["page_size"] == 20
    assert data["total_pages"] == 1


def test_generate_custom_page_size():
    response = client.post("/generate?page_size=5", json={})
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 5
    assert data["total"] == 5
    assert data["page_size"] == 5


def test_generate_custom_page():
    response = client.post("/generate?page=3", json={})
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 3


def test_generate_custom_token_length():
    response = client.post("/generate?page_size=3", json={"length": 10})
    assert response.status_code == 200
    data = response.json()
    assert all(len(token) == 10 for token in data["items"])


def test_generate_page_size_min():
    response = client.post("/generate?page_size=1", json={})
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1


def test_generate_page_size_max():
    response = client.post("/generate?page_size=100", json={})
    assert response.status_code == 200
    assert len(response.json()["items"]) == 100


def test_generate_invalid_page_zero():
    response = client.post("/generate?page=0", json={})
    assert response.status_code == 422


def test_generate_invalid_page_size_zero():
    response = client.post("/generate?page_size=0", json={})
    assert response.status_code == 422


def test_generate_invalid_page_size_over_max():
    response = client.post("/generate?page_size=101", json={})
    assert response.status_code == 422
