from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


class TaskRepository(Protocol):
    def create(self, data: TaskCreate) -> TaskRead: ...
    def get(self, task_id: UUID) -> TaskRead | None: ...
    def list(self, done: bool | None, limit: int, offset: int) -> list[TaskRead]: ...
    def update(self, task_id: UUID, patch: TaskUpdate) -> TaskRead | None: ...
    def delete(self, task_id: UUID) -> bool: ...


class InMemoryTaskRepository:
    """Adapter bọc store in-memory hiện tại để sau này thay DB repo dễ hơn."""

    def __init__(self, store):
        self._store = store

    def create(self, data: TaskCreate) -> TaskRead:
        return self._store.create(data)

    def get(self, task_id: UUID) -> TaskRead | None:
        return self._store.get(task_id)

    def list(self, done: bool | None, limit: int, offset: int) -> list[TaskRead]:
        return self._store.list(done=done, limit=limit, offset=offset)

    def update(self, task_id: UUID, patch: TaskUpdate) -> TaskRead | None:
        return self._store.update(task_id, patch)

    def delete(self, task_id: UUID) -> bool:
        return self._store.delete(task_id)
