from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from typing import Optional

from ..database.database import get_session
from ..models.user import User
from ..models.task import TaskCreate, TaskUpdate, TaskPatch
from ..schemas.task import TaskRead, TaskListResponse
from ..auth.jwt import get_current_active_user
from ..services import task_service

# -------------------- Rate Limiter --------------------
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


# -------------------- Get Tasks --------------------
@router.get("/tasks", response_model=TaskListResponse)
@limiter.limit("30/minute")
async def get_tasks(
    request: Request,
    current_user: User = Depends(get_current_active_user),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    limit: int = Query(50, ge=1, le=100, description="Number of tasks to return"),
    offset: int = Query(0, ge=0, description="Number of tasks to skip"),
    db: Session = Depends(get_session)
):
    """
    Get all tasks for the current user with optional completion filter
    """
    tasks, total = task_service.get_user_tasks(
        db=db,
        user_id=current_user.id,
        completed=completed,
        limit=limit,
        offset=offset
    )

    return TaskListResponse(
        tasks=tasks,
        total=total,
        limit=limit,
        offset=offset
    )


# -------------------- Create Task --------------------
@router.post("/tasks", response_model=TaskRead)
@limiter.limit("20/minute")
async def create_task(
    request: Request,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Create a new task for the current user
    """
    return task_service.create_task(
        db=db,
        user_id=current_user.id,
        task_data=task_data
    )


# -------------------- Get Single Task --------------------
@router.get("/tasks/{task_id}", response_model=TaskRead)
@limiter.limit("50/minute")
async def get_task(
    request: Request,
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Get a single task by ID
    """
    task = task_service.get_task_by_id(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


# -------------------- Update Task (PUT) --------------------
@router.put("/tasks/{task_id}", response_model=TaskRead)
@limiter.limit("15/minute")
async def update_task(
    request: Request,
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Fully update a task by ID
    """
    task = task_service.update_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        task_data=task_data
    )

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


# -------------------- Patch Task --------------------
@router.patch("/tasks/{task_id}", response_model=TaskRead)
@limiter.limit("20/minute")
async def patch_task(
    request: Request,
    task_id: str,
    task_data: TaskPatch,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Partially update a task by ID
    """
    task = task_service.patch_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        task_data=task_data
    )

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return task


# -------------------- Delete Task --------------------
@router.delete("/tasks/{task_id}")
@limiter.limit("10/minute")
async def delete_task(
    request: Request,
    task_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_session)
):
    """
    Hard delete a task by ID
    """
    success = task_service.delete_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return {"message": "Task deleted successfully"}
