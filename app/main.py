from fastapi import FastAPI

from app.api.v1.tasks import router as tasks_router

app = FastAPI(title="To-do API", version="0.1.0")

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
