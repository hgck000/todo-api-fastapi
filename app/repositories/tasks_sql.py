from __future__ import annotations

from uuid import UUID

from sqlmodel import Session, select

from app.models.task import Task, utcnow
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


class SQLTaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: TaskCreate) -> TaskRead:
        db_task = Task.model_validate(data)
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return TaskRead.model_validate(db_task)

    def get(self, task_id: UUID) -> TaskRead | None:
        db_task = self.session.get(Task, task_id)
        return TaskRead.model_validate(db_task) if db_task else None

    def list(self, done: bool | None, limit: int, offset: int) -> list[TaskRead]:
        stmt = select(Task)

        if done is not None:
            stmt = stmt.where(Task.done == done)

        stmt = stmt.order_by(Task.created_at).offset(offset).limit(limit)
        rows = self.session.exec(stmt).all()
        return [TaskRead.model_validate(x) for x in rows]

    def update(self, task_id: UUID, patch: TaskUpdate) -> TaskRead | None:
        db_task = self.session.get(Task, task_id)
        if not db_task:
            return None

        patch_data = patch.model_dump(exclude_unset=True)
        db_task.sqlmodel_update(patch_data)
        db_task.updated_at = utcnow()

        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return TaskRead.model_validate(db_task)

    def delete(self, task_id: UUID) -> bool:
        db_task = self.session.get(Task, task_id)
        if not db_task:
            return False

        self.session.delete(db_task)
        self.session.commit()
        return True
