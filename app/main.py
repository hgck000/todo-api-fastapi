from fastapi import FastAPI

from app.api.v1.tasks import router as tasks_router
from app.db.session import init_db

app = FastAPI(title="To-do API", version="0.1.0")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
