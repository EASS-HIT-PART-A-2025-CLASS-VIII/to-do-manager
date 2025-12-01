from fastapi.testclient import TestClient

from app.main import app, repo  # repo is the TaskRepository instance in main.py


client = TestClient(app)


def setup_function() -> None:
    """
    pytest will run this before each test in this module.
    It clears the in-memory repo so tests don't depend on order.
    """
    repo.reset()


def test_list_tasks_initially_empty():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task():
    payload = {
        "title": "Finish FastAPI exercise",
        "description": "Implement EX1 tasks backend",
        "status": "todo",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["id"] == 1
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == "todo"
    assert "created_at" in data


def test_get_task():
    payload = {"title": "Write tests", "status": "in_progress"}
    create_resp = client.post("/tasks", json=payload)
    assert create_resp.status_code == 201
    created = create_resp.json()
    task_id = created["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Write tests"
    assert data["status"] == "in_progress"


def test_update_task():
    create_resp = client.post(
        "/tasks",
        json={"title": "Old title", "status": "todo"},
    )
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    update_payload = {
        "title": "New title",
        "status": "done",
    }
    update_resp = client.put(f"/tasks/{task_id}", json=update_payload)
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["id"] == task_id
    assert data["title"] == "New title"
    assert data["status"] == "done"


def test_delete_task():
    create_resp = client.post(
        "/tasks",
        json={"title": "To be deleted", "status": "todo"},
    )
    assert create_resp.status_code == 201
    task_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/tasks/{task_id}")
    assert delete_resp.status_code == 200

    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_create_task_rejects_invalid_status():
    payload = {
        "title": "Invalid status task",
        "description": "This should fail",
        "status": "not_a_real_status",
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["detail"][0]["loc"][-1] == "status"

def test_update_task_rejects_invalid_status():
    create_resp = client.post(
        "/tasks",
        json={"title": "Task", "status": "todo"},
    )
    task_id = create_resp.json()["id"]

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "invalid_status"},
    )
    assert response.status_code == 422
