from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict
from uuid import UUID, uuid4

from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class InMemoryTaskStore:
    items: Dict[UUID, TaskRead]

    def __init__(self) -> None:
        self.items = {}

    def create(self, data: TaskCreate) -> TaskRead:
        now = utcnow()
        task = TaskRead(
            id=uuid4(),
            title=data.title,
            description=data.description,
            done=data.done,
            created_at=now,
            updated_at=now,
        )
        self.items[task.id] = task
        return task

    def get(self, task_id: UUID) -> TaskRead | None:
        return self.items.get(task_id)

    def list(self, done: bool | None, limit: int, offset: int) -> list[TaskRead]:
        values = list(self.items.values())

        if done is not None:
            values = [t for t in values if t.done == done]

        # sort ổn định theo created_at (cho predictable)
        values.sort(key=lambda t: t.created_at)

        return values[offset : offset + limit]

    def update(self, task_id: UUID, patch: TaskUpdate) -> TaskRead | None:
        task = self.items.get(task_id)
        if task is None:
            return None

        data = task.model_dump()
        patch_data = patch.model_dump(exclude_unset=True)

        for k, v in patch_data.items():
            data[k] = v

        data["updated_at"] = utcnow()
        updated = TaskRead(**data)
        self.items[task_id] = updated
        return updated

    def delete(self, task_id: UUID) -> bool:
        return self.items.pop(task_id, None) is not None


store = InMemoryTaskStore()
