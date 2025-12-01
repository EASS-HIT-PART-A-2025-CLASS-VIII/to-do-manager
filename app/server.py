from datetime import datetime
from typing import List

from .models import Task, TaskCreate, TaskUpdate
from .exceptions import TaskNotFoundError, RepositoryError


class TaskRepository:
    """
    In-memory repository for tasks.
    """

    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    # --- CRUD operations ---

    def list_tasks(self) -> List[Task]:
        """
        Return all tasks in the repository.
        """
        return list(self._tasks)

    def get_task(self, task_id: int) -> Task:
        """
        Retrieve a single task by ID.

        :raises TaskNotFoundError: if the task does not exist.
        """
        task = next((t for t in self._tasks if t.id == task_id), None)
        if task is None:
            raise TaskNotFoundError()
        return task

    def create_task(self, data: TaskCreate) -> Task:
        """
        Create and store a new task.

        :raises RepositoryError: for unexpected errors when creating the task.
        """
        try:
            task = Task(
                id=self._next_id,
                created_at=datetime.utcnow(),
                **data.model_dump(),
            )
            self._next_id += 1
            self._tasks.append(task)
            return task
        except Exception as exc:
            raise RepositoryError(str(exc)) from exc

    def update_task(self, task_id: int, data: TaskUpdate) -> Task:
        """
        Update an existing task.

        :raises TaskNotFoundError: if the task does not exist.
        :raises RepositoryError: for unexpected errors during update.
        """
        existing = self.get_task(task_id)

        try:
            update_data = data.model_dump(exclude_unset=True)
            updated = existing.model_copy(update=update_data)

            idx = next(i for i, t in enumerate(self._tasks) if t.id == task_id)
            self._tasks[idx] = updated
            return updated
        except TaskNotFoundError:
            raise
        except Exception as exc:
            raise RepositoryError(str(exc)) from exc

    def delete_task(self, task_id: int) -> None:
        """
        Delete a task by ID.

        :raises TaskNotFoundError: if the task does not exist.
        :raises RepositoryError: for unexpected errors during delete.
        """
        _ = self.get_task(task_id)

        try:
            self._tasks = [t for t in self._tasks if t.id != task_id]
        except Exception as exc:
            raise RepositoryError(str(exc)) from exc

    # --- Helpers for tests ---

    def reset(self) -> None:
        """
        Clear all tasks and reset ID counter.
        Useful for tests so they don't depend on order.
        """
        self._tasks = []
        self._next_id = 1
