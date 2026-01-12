"""
Complete CRUD endpoint example for Tasks resource.

This file demonstrates all CRUD operations:
- POST /tasks - Create new task
- GET /tasks - List tasks with pagination
- GET /tasks/{id} - Get specific task
- PATCH /tasks/{id} - Update task
- DELETE /tasks/{id} - Delete task

Copy and adapt this pattern for other resources.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, col
from typing import List, Optional

from app.core.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
# from app.api.deps import get_current_user  # For authentication
# from app.models.user import User

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with the provided information"
)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session),
    # current_user: User = Depends(get_current_user),  # Uncomment for auth
):
    """
    Create a new task.

    - **title**: Task title (required, max 100 characters)
    - **description**: Detailed description (optional)
    - **status**: Task status (default: "todo")
    - **priority**: Priority level 1-5 (default: 3)
    """
    # Create task
    task = Task(**task_in.model_dump())

    # Set user_id if authenticated
    # task.user_id = current_user.id

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.get(
    "/",
    response_model=List[TaskResponse],
    summary="List tasks",
    description="Retrieve a list of tasks with optional filtering and pagination"
)
def list_tasks(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of items to return"),
    status_filter: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[int] = Query(None, ge=1, le=5, description="Filter by priority"),
    search: Optional[str] = Query(None, min_length=1, description="Search in title"),
    session: Session = Depends(get_session),
    # current_user: User = Depends(get_current_user),  # Uncomment for auth
):
    """
    List tasks with pagination and filtering.

    Returns a list of tasks matching the specified filters.
    """
    # Build query
    statement = select(Task)

    # Apply filters
    # if current_user:  # Filter by user if authenticated
    #     statement = statement.where(Task.user_id == current_user.id)

    if status_filter:
        statement = statement.where(Task.status == status_filter)

    if priority:
        statement = statement.where(Task.priority == priority)

    if search:
        statement = statement.where(col(Task.title).contains(search))

    # Apply pagination
    statement = statement.offset(skip).limit(limit)

    # Execute query
    tasks = session.exec(statement).all()

    return tasks


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID"
)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    # current_user: User = Depends(get_current_user),  # Uncomment for auth
):
    """
    Get a specific task by ID.

    Returns 404 if task not found.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check ownership if authenticated
    # if current_user and task.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to access this task"
    #     )

    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update task",
    description="Update an existing task (partial update)"
)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: Session = Depends(get_session),
    # current_user: User = Depends(get_current_user),  # Uncomment for auth
):
    """
    Update a task.

    Only provided fields will be updated (partial update).
    Returns 404 if task not found.
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check ownership if authenticated
    # if current_user and task.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to update this task"
    #     )

    # Update only provided fields
    update_data = task_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete task",
    description="Delete an existing task"
)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    # current_user: User = Depends(get_current_user),  # Uncomment for auth
):
    """
    Delete a task.

    Returns 404 if task not found.
    Returns 204 No Content on success (no response body).
    """
    task = session.get(Task, task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    # Check ownership if authenticated
    # if current_user and task.user_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Not authorized to delete this task"
    #     )

    session.delete(task)
    session.commit()

    return None  # 204 No Content


# Optional: Additional endpoints

@router.get(
    "/status/{status}",
    response_model=List[TaskResponse],
    summary="Get tasks by status"
)
def get_tasks_by_status(
    status: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: Session = Depends(get_session)
):
    """Get all tasks with a specific status."""
    statement = (
        select(Task)
        .where(Task.status == status)
        .offset(skip)
        .limit(limit)
    )
    tasks = session.exec(statement).all()
    return tasks


# To use this router in your app:
"""
# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import tasks

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# app/main.py
from app.api.v1.api import api_router

app.include_router(api_router, prefix="/api/v1")

# URLs will be:
# POST   /api/v1/tasks
# GET    /api/v1/tasks
# GET    /api/v1/tasks/{id}
# PATCH  /api/v1/tasks/{id}
# DELETE /api/v1/tasks/{id}
"""
