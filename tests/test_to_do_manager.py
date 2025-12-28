import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.models.task_db import Base


# Setup a dedicated test database (in-memory SQLite for speed)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Creates tables before each test and drops them after.
    This replaces repo.reset() for the database version.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_list_tasks_initially_empty():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    payload = {
        "title": "Finish FastAPI exercise",
        "description": "Implement DB persistence",
        "status": "todo",
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["is_favorite"] is False  # Check default value
    assert "created_at" in data


def test_get_task():
    payload = {"title": "Write tests", "status": "in_progress"}
    create_resp = client.post("/tasks/", json=payload)
    task_id = create_resp.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Write tests"


def test_update_task():
    create_resp = client.post("/tasks/", json={"title": "Old title", "status": "todo"})
    task_id = create_resp.json()["id"]

    update_payload = {"title": "New title", "status": "done"}
    response = client.put(f"/tasks/{task_id}", json=update_payload)

    assert response.status_code == 200
    assert response.json()["title"] == "New title"
    assert response.json()["status"] == "done"


def test_toggle_favorite_feature():
    """Tests the standout 'Favorite' feature logic."""
    # 1. Create task
    create_resp = client.post("/tasks/", json={"title": "Important Task"})
    task_id = create_resp.json()["id"]
    assert create_resp.json()["is_favorite"] is False

    # 2. Toggle to True
    fav_resp = client.patch(f"/tasks/{task_id}/favorite")
    assert fav_resp.status_code == 200
    assert fav_resp.json()["is_favorite"] is True

    # 3. Toggle back to False
    unfav_resp = client.patch(f"/tasks/{task_id}/favorite")
    assert unfav_resp.json()["is_favorite"] is False


def test_delete_task():
    create_resp = client.post("/tasks/", json={"title": "To be deleted"})
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_create_task_rejects_invalid_status():
    payload = {"title": "Fail Task", "status": "not_real"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 422