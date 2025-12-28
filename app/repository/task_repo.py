from sqlalchemy.orm import Session
from ..models.task_db import TaskDB
from ..schemas.task_schema import TaskCreate, TaskUpdate
from ..exceptions import TaskNotFoundError, RepositoryError

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_all(self):
        return self.db.query(TaskDB).all()

    def get_by_id(self, task_id: int):
        task = self.db.query(TaskDB).filter(TaskDB.id == task_id).first()
        if not task:
            raise TaskNotFoundError()
        return task

    def create(self, data: TaskCreate):
        try:
            db_task = TaskDB(**data.model_dump())
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except Exception as e:
            raise RepositoryError(str(e))

    def update(self, task_id: int, data: TaskUpdate):
        db_task = self.get_by_id(task_id)
        try:
            update_data = data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            self.db.commit()
            self.db.refresh(db_task)
            return db_task
        except Exception as e:
            raise RepositoryError(str(e))

    def toggle_favorite(self, task_id: int):
        db_task = self.get_by_id(task_id)
        db_task.is_favorite = not db_task.is_favorite
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def delete(self, task_id: int):
        db_task = self.get_by_id(task_id)
        self.db.delete(db_task)
        self.db.commit()