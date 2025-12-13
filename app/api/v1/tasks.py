from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from app.db.in_memory import store
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate

router = APIRouter()


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> TaskRead:
    return store.create(payload)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    done: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> list[TaskRead]:
    return store.list(done=done, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID) -> TaskRead:
    task = store.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def patch_task(task_id: UUID, payload: TaskUpdate) -> TaskRead:
    updated = store.update(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID) -> None:
    ok = store.delete(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
