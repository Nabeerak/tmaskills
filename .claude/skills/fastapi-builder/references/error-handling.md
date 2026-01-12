# Error Handling in FastAPI

## Table of Contents

- [Built-in HTTP Exceptions](#built-in-http-exceptions)
- [Custom Exception Classes](#custom-exception-classes)
- [Exception Handlers](#exception-handlers)
- [Using Custom Exceptions](#using-custom-exceptions)
- [Error Response Models](#error-response-models)
- [Dependency Error Handling](#dependency-error-handling)
- [Background Task Errors](#background-task-errors)
- [Database Transaction Handling](#database-transaction-handling)
- [Logging Errors](#logging-errors)
- [Best Practices](#best-practices)

---

## Built-in HTTP Exceptions

FastAPI provides `HTTPException` for common HTTP errors.

```python
from fastapi import HTTPException, status

@router.get("/tasks/{task_id}")
def get_task(task_id: int, session: Session = Depends(get_session)):
    """Get task by ID."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task
```

### Common Status Codes

| Code | Constant | Usage |
|------|----------|-------|
| 400 | `HTTP_400_BAD_REQUEST` | Invalid input format |
| 401 | `HTTP_401_UNAUTHORIZED` | Not authenticated |
| 403 | `HTTP_403_FORBIDDEN` | Not authorized |
| 404 | `HTTP_404_NOT_FOUND` | Resource doesn't exist |
| 409 | `HTTP_409_CONFLICT` | Duplicate/constraint violation |
| 422 | `HTTP_422_UNPROCESSABLE_ENTITY` | Validation error (automatic) |
| 500 | `HTTP_500_INTERNAL_SERVER_ERROR` | Server error |

---

## Custom Exception Classes

Create domain-specific exceptions.

```python
# app/exceptions/custom.py
from fastapi import status

class AppException(Exception):
    """Base exception for application errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundException(AppException):
    """Resource not found exception."""

    def __init__(self, resource: str, resource_id: int):
        message = f"{resource} with id {resource_id} not found"
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class DuplicateException(AppException):
    """Duplicate resource exception."""

    def __init__(self, resource: str, field: str, value: str):
        message = f"{resource} with {field}='{value}' already exists"
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)

class PermissionDeniedException(AppException):
    """Permission denied exception."""

    def __init__(self, message: str = "You don't have permission to perform this action"):
        super().__init__(message, status_code=status.HTTP_403_FORBIDDEN)

class BusinessLogicException(AppException):
    """Business logic validation exception."""

    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)
```

---

## Exception Handlers

Register global exception handlers.

```python
# app/exceptions/handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.exceptions.custom import AppException

def register_exception_handlers(app):
    """Register all exception handlers."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        """Handle custom application exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.__class__.__name__,
                "message": exc.message,
                "path": str(request.url)
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Handle Pydantic validation errors."""
        errors = []
        for error in exc.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "message": "Request validation failed",
                "errors": errors,
                "path": str(request.url)
            }
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        """Handle database integrity errors."""
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "IntegrityError",
                "message": "Database constraint violation",
                "detail": str(exc.orig),
                "path": str(request.url)
            }
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
        """Handle general database errors."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "DatabaseError",
                "message": "Database operation failed",
                "path": str(request.url)
            }
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Catch-all for unhandled exceptions."""
        # Log the full error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Unhandled exception: {exc}", exc_info=True)

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred",
                "path": str(request.url)
            }
        )

# In main.py
from app.exceptions.handlers import register_exception_handlers

app = FastAPI()
register_exception_handlers(app)
```

---

## Using Custom Exceptions

```python
# app/api/v1/endpoints/tasks.py
from app.exceptions.custom import NotFoundException, DuplicateException, PermissionDeniedException

@router.post("/", response_model=TaskResponse)
def create_task(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create task."""
    # Check for duplicate title
    existing = session.exec(
        select(Task).where(Task.title == task_in.title)
    ).first()

    if existing:
        raise DuplicateException("Task", "title", task_in.title)

    # Create task
    task = Task(**task_in.model_dump(), user_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get task."""
    task = session.get(Task, task_id)

    if not task:
        raise NotFoundException("Task", task_id)

    # Check ownership
    if task.user_id != current_user.id:
        raise PermissionDeniedException("You can only view your own tasks")

    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete task."""
    task = session.get(Task, task_id)

    if not task:
        raise NotFoundException("Task", task_id)

    if task.user_id != current_user.id:
        raise PermissionDeniedException()

    # Business logic validation
    if task.status == "completed":
        raise BusinessLogicException("Cannot delete completed tasks")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}
```

---

## Error Response Models

Define consistent error response schemas.

```python
# app/schemas/error.py
from pydantic import BaseModel
from typing import List, Optional

class ErrorDetail(BaseModel):
    """Individual error detail."""
    field: str
    message: str
    type: str

class ErrorResponse(BaseModel):
    """Standard error response."""
    error: str
    message: str
    path: str
    errors: Optional[List[ErrorDetail]] = None

# Usage in OpenAPI docs
@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    responses={
        404: {"model": ErrorResponse, "description": "Task not found"},
        403: {"model": ErrorResponse, "description": "Permission denied"}
    }
)
def get_task(task_id: int):
    ...
```

---

## Dependency Error Handling

Handle errors in dependencies.

```python
# app/api/deps.py
from fastapi import Depends, HTTPException
from sqlmodel import Session

def get_task_or_404(
    task_id: int,
    session: Session = Depends(get_session)
) -> Task:
    """Get task or raise 404."""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found"
        )
    return task

# Use in endpoint
@router.get("/{task_id}")
def get_task(task: Task = Depends(get_task_or_404)):
    """Get task (404 handled by dependency)."""
    return task

@router.patch("/{task_id}")
def update_task(
    task_in: TaskUpdate,
    task: Task = Depends(get_task_or_404),
    session: Session = Depends(get_session)
):
    """Update task."""
    for key, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

---

## Background Task Errors

Handle errors in background tasks.

```python
from fastapi import BackgroundTasks
import logging

logger = logging.getLogger(__name__)

def send_email_with_error_handling(to: str, subject: str, body: str):
    """Send email with error handling."""
    try:
        # Email sending logic
        send_email(to, subject, body)
        logger.info(f"Email sent to {to}")
    except Exception as e:
        # Log error but don't fail the request
        logger.error(f"Failed to send email to {to}: {e}")

@router.post("/tasks")
def create_task(
    task_in: TaskCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create task and send notification."""
    task = Task(**task_in.model_dump(), user_id=current_user.id)
    session.add(task)
    session.commit()
    session.refresh(task)

    # Send notification (errors logged but don't affect response)
    background_tasks.add_task(
        send_email_with_error_handling,
        current_user.email,
        "Task Created",
        f"Task '{task.title}' created successfully"
    )

    return task
```

---

## Database Transaction Handling

Handle database errors with transactions.

```python
from sqlalchemy.exc import IntegrityError

@router.post("/tasks")
def create_task(
    task_in: TaskCreate,
    session: Session = Depends(get_session)
):
    """Create task with transaction handling."""
    try:
        task = Task(**task_in.model_dump())
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except IntegrityError as e:
        session.rollback()
        if "unique constraint" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Task with this title already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
    except Exception as e:
        session.rollback()
        raise
```

---

## Logging Errors

Log errors for debugging and monitoring.

```python
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_errors(request: Request, call_next):
    """Log all errors."""
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(
            f"Error processing request: {request.method} {request.url}",
            exc_info=True,
            extra={
                "method": request.method,
                "url": str(request.url),
                "client": request.client.host if request.client else None
            }
        )
        raise
```

---

## Best Practices

### 1. Use Specific Exceptions
```python
# ❌ Generic
raise HTTPException(status_code=404, detail="Not found")

# ✅ Specific
raise NotFoundException("Task", task_id)
```

### 2. Don't Expose Internal Details
```python
# ❌ Exposes internal error
except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

# ✅ Generic message, log details
except Exception as e:
    logger.error(f"Internal error: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal server error")
```

### 3. Return Consistent Error Format
All errors should follow same structure:
```json
{
    "error": "ErrorType",
    "message": "Human-readable message",
    "path": "/api/v1/tasks/123"
}
```

### 4. Log But Don't Expose
```python
try:
    # Database operation
    ...
except SQLAlchemyError as e:
    logger.error(f"Database error: {e}", exc_info=True)  # Log details
    raise HTTPException(
        status_code=500,
        detail="Database error occurred"  # Generic message to user
    )
```

### 5. Handle Expected Errors Gracefully
```python
# Expected errors (business logic)
if task.status == "completed":
    raise BusinessLogicException("Cannot delete completed tasks")

# Unexpected errors (programming bugs)
try:
    result = process_data(task)
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Processing failed")
```
