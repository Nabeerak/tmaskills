"""
SQLModel database model example for Task entity.

This file shows how to define a database model with:
- Primary key
- Field constraints (length, unique, index)
- Default values
- Timestamps
- Relationships (commented examples)

Copy and adapt this pattern for other database tables.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from enum import Enum


# Example: Enum for status field
class TaskStatus(str, Enum):
    """Task status options."""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


# Main model
class Task(SQLModel, table=True):
    """
    Task database model.

    Represents a task in the tasks table.
    """

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required fields
    title: str = Field(
        max_length=100,
        index=True,  # Index for searching
        description="Task title"
    )

    # Optional fields
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Detailed task description"
    )

    # Fields with default values
    status: str = Field(
        default=TaskStatus.TODO.value,
        max_length=20,
        index=True,  # Index for filtering
        description="Task status"
    )

    priority: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Priority level (1=low, 5=urgent)"
    )

    is_completed: bool = Field(default=False)

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,  # Index for sorting
        description="Creation timestamp"
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        description="Last update timestamp"
    )

    # Foreign key example (uncomment if needed)
    # user_id: Optional[int] = Field(
    #     default=None,
    #     foreign_key="user.id",
    #     index=True
    # )

    # Relationship example (uncomment if needed)
    # user: Optional["User"] = Relationship(back_populates="tasks")

    # Config
    class Config:
        """Model configuration."""
        # JSON schema customization for OpenAPI docs
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete project",
                "description": "Finish the project by Friday",
                "status": "todo",
                "priority": 4,
                "is_completed": False,
                "created_at": "2025-01-10T10:00:00Z",
                "updated_at": None
            }
        }


# Example: Model with relationship
"""
from sqlmodel import Relationship
from typing import List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    hashed_password: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # One-to-many relationship
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # Many-to-one relationship
    user: Optional[User] = Relationship(back_populates="tasks")
"""


# Example: Many-to-many relationship
"""
# Link table
class TaskTagLink(SQLModel, table=True):
    task_id: Optional[int] = Field(
        default=None,
        foreign_key="task.id",
        primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None,
        foreign_key="tag.id",
        primary_key=True
    )

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    # Many-to-many relationship
    tags: List["Tag"] = Relationship(
        back_populates="tasks",
        link_model=TaskTagLink
    )

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, max_length=50)

    # Many-to-many relationship
    tasks: List[Task] = Relationship(
        back_populates="tags",
        link_model=TaskTagLink
    )
"""


# Example: Computed property
"""
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    status: str

    @property
    def is_completed(self) -> bool:
        return self.status == "done"

    @property
    def status_display(self) -> str:
        return self.status.replace("_", " ").title()
"""


# Example: Table configuration
"""
class Task(SQLModel, table=True):
    __tablename__ = "tasks"  # Custom table name

    __table_args__ = (
        # Composite unique constraint
        UniqueConstraint("user_id", "title", name="unique_user_task"),
        # Check constraint
        CheckConstraint("priority >= 1 AND priority <= 5", name="priority_range"),
        # Index
        Index("idx_status_priority", "status", "priority"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    status: str
    priority: int
"""
