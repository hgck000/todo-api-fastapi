from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from app.db.session import get_session
from app.repositories.tasks_sql import SQLTaskRepository
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.tasks import TaskService

router = APIRouter()


def get_service(session: Session = Depends(get_session)) -> TaskService:
    repo = SQLTaskRepository(session)
    return TaskService(repo)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, service: TaskService = Depends(get_service)) -> TaskRead:
    return service.create_task(payload)


@router.get("", response_model=list[TaskRead])
def list_tasks(
    done: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: TaskService = Depends(get_service),
) -> list[TaskRead]:
    return service.list_tasks(done=done, limit=limit, offset=offset)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID, service: TaskService = Depends(get_service)) -> TaskRead:
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def patch_task(task_id: UUID, payload: TaskUpdate, service: TaskService = Depends(get_service)) -> TaskRead:
    updated = service.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: UUID, service: TaskService = Depends(get_service)) -> None:
    ok = service.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
