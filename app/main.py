from typing import List

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .models import Task, TaskCreate, TaskUpdate
from .server import TaskRepository
from .exceptions import TaskNotFoundError, RepositoryError

app = FastAPI(
    title="Task Service",
    description="Simple FastAPI microservice providing CRUD for tasks.",
    version="0.1.0",
)

# In-memory repository instance
repo = TaskRepository()



@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    """
    List all tasks.
    """
    return repo.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    """
    Retrieve a single task by ID.
    Raises TaskNotFoundError if the task does not exist.
    """
    return repo.get_task(task_id)


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate) -> Task:
    """
    Create a new task.
    """
    return repo.create_task(task_in)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_in: TaskUpdate) -> Task:
    """
    Update an existing task.
    Raises TaskNotFoundError if task does not exist.
    """
    return repo.update_task(task_id, task_in)


@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int):
    """
    Delete a task.
    Raises TaskNotFoundError if task does not exist.
    """
    repo.delete_task(task_id)
    return {"message": f"Task {task_id} deleted successfully"}


@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Task not found"},
    )


@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Repository error: {str(exc)}"},
    )
