# CRUD Patterns in FastAPI

## Table of Contents

- [Standard CRUD Operations](#standard-crud-operations)
- [Pattern 1: Direct in Endpoints (Simple)](#pattern-1-direct-in-endpoints-simple)
- [Pattern 2: Service Layer (Recommended)](#pattern-2-service-layer-recommended)
- [Advanced Patterns](#advanced-patterns)
- [HTTP Status Codes](#http-status-codes)

---

## Standard CRUD Operations

Every resource typically needs these five operations:

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| Create | POST | `/items` | Create new item |
| Read (list) | GET | `/items` | Get multiple items |
| Read (single) | GET | `/items/{id}` | Get specific item |
| Update | PUT/PATCH | `/items/{id}` | Update item |
| Delete | DELETE | `/items/{id}` | Delete item |

---

## Pattern 1: Direct in Endpoints (Simple)

For simple APIs, implement CRUD directly in route handlers.

```python
# app/api/v1/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session)
) -> Task:
    """Create a new task."""
    task = Task(**task_in.model_dump())
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
) -> List[Task]:
    """Get all tasks with pagination."""
    statement = select(Task).offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
) -> Task:
    """Get task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: Session = Depends(get_session)
) -> Task:
    """Update task (partial)."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields
    update_data = task_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Delete task."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    session.delete(task)
    session.commit()
    return None
```

---

## Pattern 2: Service Layer (Recommended)

For complex logic, separate CRUD into service layer.

### Generic CRUD Base Class

```python
# app/crud/base.py
from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlmodel import SQLModel, Session, select
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic CRUD operations."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, session: Session, id: Any) -> Optional[ModelType]:
        """Get single item by ID."""
        return session.get(self.model, id)

    def get_multi(
        self,
        session: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Get multiple items with pagination."""
        statement = select(self.model).offset(skip).limit(limit)
        return session.exec(statement).all()

    def create(self, session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """Create new item."""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self,
        session: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:
        """Update item."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def delete(self, session: Session, *, id: Any) -> ModelType:
        """Delete item."""
        obj = session.get(self.model, id)
        session.delete(obj)
        session.commit()
        return obj
```

### Specific CRUD Class

```python
# app/crud/task.py
from sqlmodel import Session, select
from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    """CRUD operations for Task."""

    def get_by_user(
        self,
        session: Session,
        *,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Get tasks by user ID."""
        statement = (
            select(Task)
            .where(Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()

    def get_by_status(
        self,
        session: Session,
        *,
        status: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Get tasks by status."""
        statement = (
            select(Task)
            .where(Task.status == status)
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()

    def search(
        self,
        session: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """Search tasks by title."""
        statement = (
            select(Task)
            .where(Task.title.contains(query))
            .offset(skip)
            .limit(limit)
        )
        return session.exec(statement).all()

# Create instance
crud_task = CRUDTask(Task)
```

### Using in Endpoints

```python
# app/api/v1/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List

from app.core.database import get_session
from app.crud.task import crud_task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session)
):
    """Create task."""
    return crud_task.create(session, obj_in=task_in)

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """List tasks."""
    return crud_task.get_multi(session, skip=skip, limit=limit)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Get task."""
    task = crud_task.get(session, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    session: Session = Depends(get_session)
):
    """Update task."""
    task = crud_task.get(session, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return crud_task.update(session, db_obj=task, obj_in=task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    session: Session = Depends(get_session)
):
    """Delete task."""
    task = crud_task.get(session, id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    crud_task.delete(session, id=task_id)
    return None
```

---

## Advanced Patterns

### Filtering and Searching

```python
from sqlmodel import col

@router.get("/search", response_model=List[TaskResponse])
def search_tasks(
    q: Optional[str] = Query(None, min_length=1),
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """Search and filter tasks."""
    statement = select(Task)

    if q:
        statement = statement.where(col(Task.title).contains(q))
    if status:
        statement = statement.where(Task.status == status)
    if user_id:
        statement = statement.where(Task.user_id == user_id)

    statement = statement.offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks
```

### Sorting

```python
from sqlmodel import col

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    sort_by: str = Query("created_at", regex="^(title|created_at|status)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    session: Session = Depends(get_session)
):
    """List tasks with sorting."""
    statement = select(Task)

    # Apply sorting
    column = getattr(Task, sort_by)
    if order == "desc":
        statement = statement.order_by(col(column).desc())
    else:
        statement = statement.order_by(column)

    statement = statement.offset(skip).limit(limit)
    tasks = session.exec(statement).all()
    return tasks
```

### Pagination Response

```python
# app/schemas/common.py
from pydantic import BaseModel
from typing import Generic, TypeVar, List

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response with metadata."""
    items: List[T]
    total: int
    skip: int
    limit: int

# Usage in endpoint
@router.get("/", response_model=PaginatedResponse[TaskResponse])
def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """List tasks with pagination metadata."""
    # Get total count
    count_statement = select(func.count()).select_from(Task)
    total = session.exec(count_statement).one()

    # Get items
    statement = select(Task).offset(skip).limit(limit)
    items = session.exec(statement).all()

    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }
```

### Bulk Operations

```python
@router.post("/bulk", response_model=List[TaskResponse])
def create_tasks_bulk(
    tasks_in: List[TaskCreate],
    session: Session = Depends(get_session)
):
    """Create multiple tasks."""
    tasks = [Task(**task.model_dump()) for task in tasks_in]
    session.add_all(tasks)
    session.commit()
    for task in tasks:
        session.refresh(task)
    return tasks

@router.delete("/bulk", status_code=status.HTTP_204_NO_CONTENT)
def delete_tasks_bulk(
    task_ids: List[int],
    session: Session = Depends(get_session)
):
    """Delete multiple tasks."""
    statement = select(Task).where(col(Task.id).in_(task_ids))
    tasks = session.exec(statement).all()

    for task in tasks:
        session.delete(task)

    session.commit()
    return None
```

---

## HTTP Status Codes

Use appropriate status codes for each operation:

| Operation | Success Code | Description |
|-----------|--------------|-------------|
| POST (create) | 201 CREATED | Resource created |
| GET (single) | 200 OK | Resource found |
| GET (list) | 200 OK | Resources retrieved |
| PUT/PATCH | 200 OK | Resource updated |
| DELETE | 204 NO CONTENT | Resource deleted (no body) |

Error codes:
- 400 BAD REQUEST: Invalid input
- 401 UNAUTHORIZED: Not authenticated
- 403 FORBIDDEN: Not authorized
- 404 NOT FOUND: Resource doesn't exist
- 409 CONFLICT: Duplicate/constraint violation
- 422 UNPROCESSABLE ENTITY: Validation error (automatic)
- 500 INTERNAL SERVER ERROR: Server error
