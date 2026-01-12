"""
Pydantic schemas for Task API request/response validation.
Separates API layer from database models for security and flexibility.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    """Shared properties for Task schemas."""
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    # Title is required, others optional with defaults from TaskBase

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate title is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write comprehensive API documentation",
                "status": "pending",
                "priority": "medium"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. All fields optional."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: Optional[str]) -> Optional[str]:
        """Validate title if provided."""
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated task title",
                "status": "in_progress",
                "priority": "high"
            }
        }


class TaskResponse(TaskBase):
    """Schema for task responses including database fields."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows creation from ORM models
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication",
                "status": "in_progress",
                "priority": "high",
                "created_at": "2024-01-10T10:30:00Z",
                "updated_at": "2024-01-10T14:20:00Z"
            }
        }


class TaskListResponse(BaseModel):
    """Schema for paginated task list responses."""
    items: list[TaskResponse]
    total: int
    skip: int
    limit: int

    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {
                        "id": 1,
                        "title": "Task 1",
                        "description": "Description 1",
                        "status": "pending",
                        "priority": "high",
                        "created_at": "2024-01-10T10:00:00Z",
                        "updated_at": "2024-01-10T10:00:00Z"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 100
            }
        }
