from datetime import datetime
from typing import List, Optional

from .models import Task, TaskCreate, TaskUpdate


class TaskRepository:
    """
    in-memory repository for tasks
    """

    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    # --- CRUD operations ---

    def list_tasks(self) -> List[Task]:
        return list(self._tasks)

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((t for t in self._tasks if t.id == task_id), None)

    def create_task(self, data: TaskCreate) -> Task:
        task = Task(
            id=self._next_id,
            created_at=datetime.utcnow(),
            **data.model_dump(),
        )
        self._next_id += 1
        self._tasks.append(task)
        return task

    def update_task(self, task_id: int, data: TaskUpdate) -> Optional[Task]:
        existing = self.get_task(task_id)
        if existing is None:
            return None

        update_data = data.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=update_data)

        idx = next(i for i, t in enumerate(self._tasks) if t.id == task_id)
        self._tasks[idx] = updated
        return updated

    def delete_task(self, task_id: int) -> bool:
        existing = self.get_task(task_id)
        if existing is None:
            return False

        self._tasks = [t for t in self._tasks if t.id != task_id]
        return True

    # --- Helpers for tests ---

    def reset(self) -> None:
        """
        Clear all tasks and reset ID counter
        Useful for tests so they don't depend on order
        """
        self._tasks = []
        self._next_id = 1
