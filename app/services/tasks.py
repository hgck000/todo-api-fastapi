from __future__ import annotations

from uuid import UUID

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.repositories.tasks import TaskRepository


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    def create_task(self, payload: TaskCreate) -> TaskRead:
        return self.repo.create(payload)

    def list_tasks(self, done: bool | None, limit: int, offset: int) -> list[TaskRead]:
        return self.repo.list(done=done, limit=limit, offset=offset)

    def get_task(self, task_id: UUID) -> TaskRead | None:
        return self.repo.get(task_id)

    def update_task(self, task_id: UUID, payload: TaskUpdate) -> TaskRead | None:
        return self.repo.update(task_id, payload)

    def delete_task(self, task_id: UUID) -> bool:
        return self.repo.delete(task_id)
