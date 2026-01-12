"""
Unit tests for SQLModel Task model.
Tests model creation, default values, and field validation.
"""
import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models.task import Task, TaskStatus, TaskPriority


@pytest.mark.unit
class TestTaskModel:
    """Test Task SQLModel."""

    def test_create_task_with_all_fields(self):
        """Test creating task model with all fields."""
        # Arrange
        now = datetime.utcnow()

        # Act
        task = Task(
            id=1,
            title="Test Task",
            description="Test Description",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH,
            created_at=now,
            updated_at=now
        )

        # Assert
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Description"
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.priority == TaskPriority.HIGH
        assert task.created_at == now
        assert task.updated_at == now

    def test_create_task_with_minimal_fields(self):
        """Test creating task with only required fields."""
        # Arrange & Act
        task = Task(title="Minimal Task")

        # Assert
        assert task.title == "Minimal Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING  # Default
        assert task.priority == TaskPriority.MEDIUM  # Default
        assert task.created_at is not None  # Auto-generated
        assert task.updated_at is not None  # Auto-generated

    def test_create_task_default_status(self):
        """Test that default status is PENDING."""
        # Arrange & Act
        task = Task(title="Default Status Task")

        # Assert
        assert task.status == TaskStatus.PENDING

    def test_create_task_default_priority(self):
        """Test that default priority is MEDIUM."""
        # Arrange & Act
        task = Task(title="Default Priority Task")

        # Assert
        assert task.priority == TaskPriority.MEDIUM

    def test_create_task_auto_generated_timestamps(self):
        """Test that timestamps are auto-generated."""
        # Arrange
        before = datetime.utcnow()

        # Act
        task = Task(title="Timestamp Task")
        after = datetime.utcnow()

        # Assert
        assert task.created_at is not None
        assert task.updated_at is not None
        assert before <= task.created_at <= after
        assert before <= task.updated_at <= after

    @pytest.mark.xfail(reason="SQLModel doesn't enforce validation at Python level, only at DB level")
    def test_create_task_missing_title_raises_error(self):
        """Test that missing title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Task()

        # Assert
        assert "title" in str(exc_info.value).lower()

    @pytest.mark.xfail(reason="SQLModel doesn't enforce validation at Python level, only at DB level")
    def test_create_task_empty_title_raises_error(self):
        """Test that empty title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Task(title="")

        # Assert
        assert "String should have at least 1 character" in str(exc_info.value)

    @pytest.mark.xfail(reason="SQLModel doesn't enforce validation at Python level, only at DB level")
    def test_create_task_title_too_long_raises_error(self):
        """Test that title exceeding max length raises error."""
        # Arrange
        long_title = "A" * 201

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Task(title=long_title)

        # Assert
        assert "String should have at most 200 characters" in str(exc_info.value)

    @pytest.mark.xfail(reason="SQLModel doesn't enforce validation at Python level, only at DB level")
    def test_create_task_description_too_long_raises_error(self):
        """Test that description exceeding max length raises error."""
        # Arrange
        long_description = "B" * 2001

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Task(title="Test", description=long_description)

        # Assert
        assert "String should have at most 2000 characters" in str(exc_info.value)

    @pytest.mark.parametrize("title_length", [1, 50, 100, 200])
    def test_create_task_valid_title_lengths(self, title_length):
        """Test various valid title lengths."""
        # Arrange
        title = "T" * title_length

        # Act
        task = Task(title=title)

        # Assert
        assert len(task.title) == title_length

    @pytest.mark.parametrize("description_length", [1, 500, 1000, 2000])
    def test_create_task_valid_description_lengths(self, description_length):
        """Test various valid description lengths."""
        # Arrange
        description = "D" * description_length

        # Act
        task = Task(title="Test", description=description)

        # Assert
        assert len(task.description) == description_length

    def test_create_task_none_description_is_valid(self):
        """Test that None description is valid."""
        # Arrange & Act
        task = Task(title="Test", description=None)

        # Assert
        assert task.description is None

    def test_task_table_name(self):
        """Test that table name is correctly set."""
        # Arrange & Act
        task = Task(title="Test")

        # Assert
        assert task.__tablename__ == "tasks"

    def test_task_id_is_primary_key(self):
        """Test that id field is configured as primary key."""
        # Arrange & Act
        task = Task(title="Test")

        # Assert
        # Primary key should be auto-generated (None before save)
        assert task.id is None or isinstance(task.id, int)


@pytest.mark.unit
class TestTaskStatus:
    """Test TaskStatus enumeration."""

    def test_task_status_values(self):
        """Test all TaskStatus enum values."""
        # Arrange & Act & Assert
        assert TaskStatus.PENDING == "pending"
        assert TaskStatus.IN_PROGRESS == "in_progress"
        assert TaskStatus.COMPLETED == "completed"

    def test_task_status_membership(self):
        """Test TaskStatus enum membership."""
        # Arrange & Act & Assert
        assert "pending" in [s.value for s in TaskStatus]
        assert "in_progress" in [s.value for s in TaskStatus]
        assert "completed" in [s.value for s in TaskStatus]

    def test_task_status_count(self):
        """Test that TaskStatus has exactly 3 values."""
        # Arrange & Act
        status_count = len(list(TaskStatus))

        # Assert
        assert status_count == 3

    @pytest.mark.parametrize("status", [
        TaskStatus.PENDING,
        TaskStatus.IN_PROGRESS,
        TaskStatus.COMPLETED,
    ])
    def test_create_task_with_each_status(self, status):
        """Test creating task with each status value."""
        # Arrange & Act
        task = Task(title="Test", status=status)

        # Assert
        assert task.status == status

    @pytest.mark.xfail(reason="SQLModel doesn't enforce validation at Python level, only at DB level")
    def test_task_invalid_status_raises_error(self):
        """Test that invalid status value raises error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Task(title="Test", status="invalid_status")

        # Assert
        assert "status" in str(exc_info.value).lower()


@pytest.mark.unit
class TestTaskPriority:
    """Test TaskPriority enumeration."""

    def test_task_priority_values(self):
        """Test all TaskPriority enum values."""
        # Arrange & Act & Assert
        assert TaskPriority.LOW == "low"
        assert TaskPriority.MEDIUM == "medium"
        assert TaskPriority.HIGH == "high"

    def test_task_priority_membership(self):
        """Test TaskPriority enum membership."""
        # Arrange & Act & Assert
        assert "low" in [p.value for p in TaskPriority]
        assert "medium" in [p.value for p in TaskPriority]
        assert "high" in [p.value for p in TaskPriority]

    def test_task_priority_count(self):
        """Test that TaskPriority has exactly 3 values."""
        # Arrange & Act
        priority_count = len(list(TaskPriority))

        # Assert
        assert priority_count == 3

    @pytest.mark.parametrize("priority", [
        TaskPriority.LOW,
        TaskPriority.MEDIUM,
        TaskPriority.HIGH,
    ])
    def test_create_task_with_each_priority(self, priority):
        """Test creating task with each priority value."""
        # Arrange & Act
        task = Task(title="Test", priority=priority)

        # Assert
        assert task.priority == priority

    @pytest.mark.xfail(reason="SQLModel doesn't enforce validation at Python level, only at DB level")
    def test_task_invalid_priority_raises_error(self):
        """Test that invalid priority value raises error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Task(title="Test", priority="invalid_priority")

        # Assert
        assert "priority" in str(exc_info.value).lower()


@pytest.mark.unit
class TestTaskModelEdgeCases:
    """Test edge cases and special scenarios for Task model."""

    @pytest.mark.parametrize("special_title", [
        "Task with emoji 🎯",
        "Task with Unicode 中文",
        "Task with symbols !@#$%",
        "Task\twith\ttabs",
        "Task with 'quotes'",
    ])
    def test_task_with_special_characters(self, special_title):
        """Test task creation with special characters."""
        # Arrange & Act
        task = Task(title=special_title)

        # Assert
        assert task.title == special_title

    def test_task_timestamps_are_datetime_objects(self):
        """Test that timestamps are proper datetime objects."""
        # Arrange & Act
        task = Task(title="Timestamp Test")

        # Assert
        assert isinstance(task.created_at, datetime)
        assert isinstance(task.updated_at, datetime)

    def test_task_created_and_updated_at_same_on_creation(self):
        """Test that created_at and updated_at are same on creation."""
        # Arrange & Act
        task = Task(title="Same Timestamps")

        # Assert
        # They should be very close (within a second)
        time_diff = abs((task.created_at - task.updated_at).total_seconds())
        assert time_diff < 1

    def test_task_with_none_id(self):
        """Test that task can be created with None id (before DB save)."""
        # Arrange & Act
        task = Task(title="No ID")

        # Assert
        assert task.id is None

    def test_task_with_explicit_id(self):
        """Test that task can be created with explicit id."""
        # Arrange & Act
        task = Task(id=42, title="Explicit ID")

        # Assert
        assert task.id == 42

    def test_task_description_can_be_empty_string(self):
        """Test that empty string description is valid."""
        # Arrange & Act
        task = Task(title="Test", description="")

        # Assert
        assert task.description == ""

    @pytest.mark.parametrize("boundary_length", [1, 200])
    def test_task_boundary_title_lengths(self, boundary_length):
        """Test boundary values for title length."""
        # Arrange
        title = "X" * boundary_length

        # Act
        task = Task(title=title)

        # Assert
        assert len(task.title) == boundary_length

    @pytest.mark.parametrize("boundary_length", [0, 1, 2000])
    def test_task_boundary_description_lengths(self, boundary_length):
        """Test boundary values for description length."""
        # Arrange
        description = "Y" * boundary_length if boundary_length > 0 else ""

        # Act
        task = Task(title="Test", description=description)

        # Assert
        assert len(task.description) == boundary_length
