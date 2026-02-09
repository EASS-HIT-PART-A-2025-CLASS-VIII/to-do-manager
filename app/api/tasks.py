from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.task_schema import Task, TaskCreate, TaskUpdate
from ..repository.task_repo import TaskRepository
from ..core.ai_services import categorize_task, generate_task_description  # ייבוא השירות החדש שתיצור

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
    """
    Create a new task with AI-powered smart categorization.
    """
    try:
        ai_data = categorize_task(task_in.title, task_in.description or "")
        task_in.category = f"{ai_data.get('emoji', '📝')} {ai_data.get('category', 'General')}"
    except Exception as e:
        print(f"AI Categorization failed: {e}")
        task_in.category = "📝 General"

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


@router.patch("/{task_id}/generate-description", response_model=Task)
def ai_description(task_id: int, db: Session = Depends(get_db)):
    repo = TaskRepository(db)
    task = repo.get_by_id(task_id)

    new_description = generate_task_description(task.title)

    updated_task = repo.update(task_id, TaskUpdate(description=new_description))
    return updated_task
