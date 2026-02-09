from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    due_date: Optional[date] = None
    category: Optional[str] = Field("📝 General", max_length=50)


class TaskCreate(TaskBase):
    """
    Fields required when creating a task
    """
    pass


class TaskUpdate(BaseModel):
    """
    Fields that may be updated. All optional so we can do partial updates
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    category: Optional[str] = Field(None, max_length=50)


class Task(TaskBase):
    """
    The full Task returned from the API
    """
    id: int
    created_at: datetime
    is_favorite: bool = False

    class Config:
        from_attributes = True
