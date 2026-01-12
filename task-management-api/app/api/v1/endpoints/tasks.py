"""
Task API endpoints with full CRUD operations.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Query
from app.api.deps import SessionDep, PaginationDep
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.models.task import TaskStatus, TaskPriority
from app.crud import task as crud
from app.exceptions.handlers import TaskNotFoundException


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task with title, description, status, and priority."
)
async def create_task(
    task_in: TaskCreate,
    session: SessionDep
) -> TaskResponse:
    """
    Create a new task.

    Args:
        task_in: Task creation data
        session: Database session

    Returns:
        Created task with generated ID and timestamps
    """
    task = await crud.create_task(session, task_in)
    return task


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get all tasks",
    description="Retrieve all tasks with pagination support. Optionally filter by status or priority."
)
async def get_tasks(
    session: SessionDep,
    pagination: PaginationDep,
    status: Optional[TaskStatus] = Query(None, description="Filter by task status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by task priority")
) -> TaskListResponse:
    """
    Retrieve all tasks with optional filtering.

    Args:
        session: Database session
        pagination: Pagination parameters (skip, limit)
        status: Optional status filter
        priority: Optional priority filter

    Returns:
        Paginated list of tasks with total count
    """
    # Filter by status if provided
    if status:
        tasks, total = await crud.get_tasks_by_status(
            session, status.value, pagination.skip, pagination.limit
        )
    # Filter by priority if provided
    elif priority:
        tasks, total = await crud.get_tasks_by_priority(
            session, priority.value, pagination.skip, pagination.limit
        )
    # No filter - get all tasks
    else:
        tasks, total = await crud.get_tasks(session, pagination.skip, pagination.limit)

    return TaskListResponse(
        items=tasks,
        total=total,
        skip=pagination.skip,
        limit=pagination.limit
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get a task by ID",
    description="Retrieve a specific task by its ID."
)
async def get_task(
    task_id: int,
    session: SessionDep
) -> TaskResponse:
    """
    Retrieve a single task by ID.

    Args:
        task_id: Task ID to retrieve
        session: Database session

    Returns:
        Task data

    Raises:
        HTTPException: 404 if task not found
    """
    task = await crud.get_task(session, task_id)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task's fields. Only provided fields will be updated."
)
async def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: SessionDep
) -> TaskResponse:
    """
    Update an existing task.

    Args:
        task_id: Task ID to update
        task_in: Task update data (only provided fields will be updated)
        session: Database session

    Returns:
        Updated task data

    Raises:
        HTTPException: 404 if task not found
    """
    task = await crud.update_task(session, task_id, task_in)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Partially update a task",
    description="Partially update a task. Same as PUT but semantically indicates partial update."
)
async def patch_task(
    task_id: int,
    task_in: TaskUpdate,
    session: SessionDep
) -> TaskResponse:
    """
    Partially update a task (same as PUT for this API).

    Args:
        task_id: Task ID to update
        task_in: Task update data
        session: Database session

    Returns:
        Updated task data

    Raises:
        HTTPException: 404 if task not found
    """
    task = await crud.update_task(session, task_id, task_in)
    if not task:
        raise TaskNotFoundException(task_id)
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    description="Delete a task by ID. Returns 204 No Content on success."
)
async def delete_task(
    task_id: int,
    session: SessionDep
) -> None:
    """
    Delete a task by ID.

    Args:
        task_id: Task ID to delete
        session: Database session

    Returns:
        None (204 No Content)

    Raises:
        HTTPException: 404 if task not found
    """
    deleted = await crud.delete_task(session, task_id)
    if not deleted:
        raise TaskNotFoundException(task_id)
