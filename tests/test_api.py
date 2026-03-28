import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Task Manager API is running"}

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_task():
    task_data = {"title": "Test Task", "priority": "high"}
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 200
    assert "message" in response.json()