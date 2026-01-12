"""
SQLModel for Task entity with database table definition.
"""
from datetime import datetime
from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel


class TaskStatus(str, Enum):
    """Task status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Task priority enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(SQLModel, table=True):
    """
    Task database model.

    Represents a task in the task management system with status tracking,
    priority levels, and automatic timestamps.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Implement user authentication",
                "description": "Add JWT-based authentication to the API",
                "status": "in_progress",
                "priority": "high",
                "created_at": "2024-01-10T10:30:00",
                "updated_at": "2024-01-10T14:20:00"
            }
        }
