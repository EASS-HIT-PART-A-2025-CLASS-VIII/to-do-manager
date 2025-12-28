from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.task_schema import Task, TaskCreate, TaskUpdate
from ..repository.task_repo import TaskRepository

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[Task])
def list_tasks(db: Session = Depends(get_db)) -> List[Task]:
    """List all tasks from the database."""
    return TaskRepository(db).list_all()


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, db: Session = Depends(get_db)) -> Task:
    """Retrieve a single task by ID."""
    return TaskRepository(db).get_by_id(task_id)


@router.post("/", response_model=Task, status_code=201)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)) -> Task:
    """Create a new task."""
    return TaskRepository(db).create(task_in)


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    """Update an existing task (supports partial updates)."""
    return TaskRepository(db).update(task_id, task_in)


@router.delete("/{task_id}", status_code=200)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    TaskRepository(db).delete(task_id)
    return {"message": f"Task {task_id} deleted successfully"}


@router.patch("/{task_id}/favorite", response_model=Task)
def toggle_task_favorite(task_id: int, db: Session = Depends(get_db)) -> Task:
    """
    Toggle the favorite status of a task.
    """
    return TaskRepository(db).toggle_favorite(task_id)
