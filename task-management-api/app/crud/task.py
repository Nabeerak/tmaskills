"""
CRUD operations for Task entity.
Handles database operations with proper async/await patterns.
"""
from typing import Optional
from datetime import datetime
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


async def create_task(session: AsyncSession, task_in: TaskCreate) -> Task:
    """
    Create a new task in the database.

    Args:
        session: Database session
        task_in: Task creation schema with validated data

    Returns:
        Created task with generated id and timestamps
    """
    task = Task(**task_in.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: int) -> Optional[Task]:
    """
    Retrieve a single task by ID.

    Args:
        session: Database session
        task_id: Task ID to retrieve

    Returns:
        Task if found, None otherwise
    """
    statement = select(Task).where(Task.id == task_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_tasks(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> tuple[list[Task], int]:
    """
    Retrieve multiple tasks with pagination and optional filtering.

    Args:
        session: Database session
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return
        status: Optional status filter
        priority: Optional priority filter

    Returns:
        Tuple of (list of tasks, total count)
    """
    # Build query with optional filters
    statement = select(Task)

    if status:
        statement = statement.where(Task.status == status)
    if priority:
        statement = statement.where(Task.priority == priority)

    # Apply pagination and ordering
    statement = statement.offset(skip).limit(limit).order_by(Task.created_at.desc())
    result = await session.execute(statement)
    tasks = result.scalars().all()

    # Get total count with same filters
    count_statement = select(Task)
    if status:
        count_statement = count_statement.where(Task.status == status)
    if priority:
        count_statement = count_statement.where(Task.priority == priority)

    count_result = await session.execute(count_statement)
    total = len(count_result.scalars().all())

    return list(tasks), total


async def get_tasks_by_status(
    session: AsyncSession,
    status: str,
    skip: int = 0,
    limit: int = 100
) -> tuple[list[Task], int]:
    """
    Retrieve tasks filtered by status.

    Args:
        session: Database session
        status: Task status to filter by
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return

    Returns:
        Tuple of (list of tasks, total count)
    """
    return await get_tasks(session, skip=skip, limit=limit, status=status)


async def get_tasks_by_priority(
    session: AsyncSession,
    priority: str,
    skip: int = 0,
    limit: int = 100
) -> tuple[list[Task], int]:
    """
    Retrieve tasks filtered by priority.

    Args:
        session: Database session
        priority: Task priority to filter by
        skip: Number of records to skip (offset)
        limit: Maximum number of records to return

    Returns:
        Tuple of (list of tasks, total count)
    """
    return await get_tasks(session, skip=skip, limit=limit, priority=priority)


async def update_task(
    session: AsyncSession,
    task_id: int,
    task_in: TaskUpdate
) -> Optional[Task]:
    """
    Update an existing task.

    Args:
        session: Database session
        task_id: Task ID to update
        task_in: Task update schema with new values

    Returns:
        Updated task if found, None otherwise
    """
    # Fetch existing task
    task = await get_task(session, task_id)
    if not task:
        return None

    # Update fields that are provided (not None)
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # Update timestamp
    task.updated_at = datetime.utcnow()

    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int) -> bool:
    """
    Delete a task by ID.

    Args:
        session: Database session
        task_id: Task ID to delete

    Returns:
        True if task was deleted, False if not found
    """
    task = await get_task(session, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True
