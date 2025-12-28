from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .api import tasks
from .models.task_db import Base
from .database import engine
from .exceptions import TaskNotFoundError, RepositoryError  # Import both

# Initialize DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Include routers
app.include_router(tasks.router)

# --- Global Exception Handlers ---

@app.exception_handler(TaskNotFoundError)
async def handle_not_found(request: Request, exc: TaskNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": "Task not found"}
    )

@app.exception_handler(RepositoryError)
async def repository_error_handler(request: Request, exc: RepositoryError):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Repository error: {str(exc)}"},
    )