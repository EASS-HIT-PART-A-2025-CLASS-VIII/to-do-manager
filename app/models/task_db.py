from sqlalchemy import Column, Integer, String, DateTime, Date, Enum as SQLEnum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from app.schemas.task_schema import TaskStatus

Base = declarative_base()

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    due_date = Column(Date)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
