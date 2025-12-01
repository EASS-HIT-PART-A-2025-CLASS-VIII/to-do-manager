from typing import List

from fastapi import FastAPI, HTTPException

from .models import Task, TaskCreate, TaskUpdate
from .repository import TaskRepository

app = FastAPI(
    title="Task Service",
    description="Simple FastAPI microservice providing CRUD for tasks.",
    version="0.1.0",
)

# In-memory repository instance (for now)
repo = TaskRepository()


@app.get("/tasks", response_model=List[Task])
def list_tasks() -> List[Task]:
    """
    List all tasks
    """
    return repo.list_tasks()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    """
    Retrieve a single task by ID
    """
    task = repo.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate) -> Task:
    """
    Create a new task
    """
    return repo.create_task(task_in)


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_in: TaskUpdate) -> Task:
    """
    Update an existing task
    """
    updated = repo.update_task(task_id, task_in)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@app.delete("/tasks/{task_id}", status_code=200)
def delete_task(task_id: int):
    """
    Delete a task
    """
    deleted = repo.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}
