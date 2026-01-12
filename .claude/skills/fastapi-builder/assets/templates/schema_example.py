"""
Pydantic schema examples for Task API.

This file shows how to define schemas for:
- Creating items (POST requests)
- Updating items (PUT/PATCH requests)
- Responding with items (GET responses)

Copy and adapt this pattern for other resources.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


# Example: Enum for validation
class TaskStatus(str, Enum):
    """Valid task status values."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


# Base schema with common fields
class TaskBase(BaseModel):
    """
    Base schema with common task fields.

    Other schemas inherit from this to avoid duplication.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Task title"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Detailed description"
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Task status"
    )
    priority: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Priority level (1-5)"
    )


# Create schema (for POST requests)
class TaskCreate(TaskBase):
    """
    Schema for creating a new task.

    All fields from TaskBase are required (or have defaults).
    """

    # Custom validation
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """Ensure title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    # Example configuration
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project proposal",
                "description": "Write and submit Q2 project proposal",
                "status": "todo",
                "priority": 4
            }
        }


# Update schema (for PATCH requests)
class TaskUpdate(BaseModel):
    """
    Schema for updating a task.

    All fields are optional for partial updates.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    is_completed: Optional[bool] = None

    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v

    class Config:
        json_schema_extra = {
            "example": {
                "status": "in_progress",
                "priority": 5
            }
        }


# Response schema (for GET responses)
class TaskResponse(TaskBase):
    """
    Schema for task in API responses.

    Includes read-only fields like id and timestamps.
    """
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Enable ORM mode to create from SQLModel instances
    class Config:
        from_attributes = True  # Was orm_mode in Pydantic v1

        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete project proposal",
                "description": "Write and submit Q2 project proposal",
                "status": "in_progress",
                "priority": 4,
                "is_completed": False,
                "created_at": "2025-01-10T10:00:00Z",
                "updated_at": "2025-01-10T15:30:00Z"
            }
        }


# Example: Nested schema with relationships
"""
from typing import List

class UserBase(BaseModel):
    email: str
    username: str

class UserResponse(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class TaskResponse(TaskBase):
    id: int
    user: UserResponse  # Nested user data

    class Config:
        from_attributes = True
"""


# Example: Schema with custom validation
"""
from pydantic import model_validator

class TaskCreate(TaskBase):
    due_date: Optional[datetime] = None

    @model_validator(mode='after')
    def validate_due_date(self) -> 'TaskCreate':
        if self.due_date and self.due_date < datetime.utcnow():
            raise ValueError('Due date must be in the future')
        return self
"""


# Example: Schema with computed fields
"""
from pydantic import computed_field

class TaskResponse(TaskBase):
    id: int
    created_at: datetime

    @computed_field
    @property
    def is_overdue(self) -> bool:
        if not self.due_date:
            return False
        return datetime.utcnow() > self.due_date and not self.is_completed
"""


# Example: List response with pagination
"""
from typing import List, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int
    has_more: bool

# Usage
@router.get("/tasks", response_model=PaginatedResponse[TaskResponse])
def get_tasks(skip: int = 0, limit: int = 100):
    ...
"""


# Example: Error response schema
"""
from typing import List, Optional

class ErrorDetail(BaseModel):
    field: str
    message: str
    type: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None

# Usage in endpoint
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
"""
