"""
Custom exception classes and handlers for the API.
Provides consistent error responses across the application.
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


class TaskNotFoundException(HTTPException):
    """Exception raised when a task is not found."""
    def __init__(self, task_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )


class DatabaseException(HTTPException):
    """Exception raised for database-related errors."""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


async def task_not_found_handler(request: Request, exc: TaskNotFoundException) -> JSONResponse:
    """Handler for TaskNotFoundException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Not Found",
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for request validation errors."""
    # Convert error details to JSON-serializable format
    errors = []
    for error in exc.errors():
        error_dict = {
            "loc": error.get("loc"),
            "msg": error.get("msg"),
            "type": error.get("type"),
        }
        # Handle ctx field which may contain non-serializable objects
        if "ctx" in error:
            ctx = error["ctx"]
            if isinstance(ctx, dict):
                error_dict["ctx"] = {k: str(v) for k, v in ctx.items()}
            else:
                error_dict["ctx"] = str(ctx)
        # Handle input field
        if "input" in error:
            try:
                error_dict["input"] = error["input"]
            except (TypeError, ValueError):
                error_dict["input"] = str(error["input"])
        errors.append(error_dict)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": errors,
            "path": str(request.url.path)
        }
    )


async def database_exception_handler(request: Request, exc: DatabaseException) -> JSONResponse:
    """Handler for database exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Database Error",
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for uncaught exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "path": str(request.url.path)
        }
    )
