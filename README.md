# Task Service – EX1 FastAPI Backend

This project implements the backend microservice for **ToDoManager**, as required in:

**EX1 – FastAPI Foundations (Backend)**

The service provides CRUD operations for managing Tasks using:

- **FastAPI**
- **Pydantic**
- **pytest + TestClient**
- **In-memory repository** (per EX1 requirement)

---

## Project Structure

```css
ToDoManager/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── repository.py
├── tests/
│   └── test_to_do_manager.py
├── requirements.txt
└── README.md
```

# 🚀 Getting Started

This project uses **uv** for environment management and dependency installation.

## 1. Create a uv virtual environment

From the project root:

```bash
uv venv
```

## 2. Activate the environment

```bash
.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

## 4. Running the API

```bash
uv run uvicorn app.main:app --reload
```

The server runs on: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs

## API Overview

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks |
| GET | `/tasks/{id}` | Retrieve a task by ID |
| POST | `/tasks` | Create a new task |
| PUT | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task by ID |

## Request/Response Examples

GET `/tasks`
```json
[
  {
    "title": "Do laundry",
    "description": "important",
    "status": "todo",
    "due_date": "2025-12-01",
    "id": 1,
    "created_at": "2025-12-01T10:16:01.071856"
  }
]
```


POST `/tasks/{id}`
```json
{
  "title": "Do laundry",
  "description": "important",
  "status": "todo",
  "due_date": "2025-12-01"
}
```

DELETE `/tasks/{id}`
```json
{
  "message": "Task 1 deleted successfully"
}
```



## Running Tests

The project uses pytest + FastAPI's TestClient.

To run the test suite:

```bash
uv run pytest
```

## Docker

This project includes a Dockerfile so the API can run inside a container.

Build the Docker image:
```bash
docker build -t todo-manager .
```
Run the container:
```bash
docker run -p 8000:8000 todo-manager
```


