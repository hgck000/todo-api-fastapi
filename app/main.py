from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.tasks import router as tasks_router
from app.db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="To-do API", version="0.1.0", lifespan=lifespan)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
