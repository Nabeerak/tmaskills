"""
Unit tests for Pydantic schemas.
Tests validation logic, field constraints, and schema behavior.
"""
import pytest
from pydantic import ValidationError

from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.models.task import TaskStatus, TaskPriority
from datetime import datetime


@pytest.mark.unit
class TestTaskCreate:
    """Test TaskCreate schema validation."""

    def test_create_task_valid_all_fields(self):
        """Test creating schema with all valid fields."""
        # Arrange & Act
        task = TaskCreate(
            title="Valid Task",
            description="Valid description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH
        )

        # Assert
        assert task.title == "Valid Task"
        assert task.description == "Valid description"
        assert task.status == TaskStatus.PENDING
        assert task.priority == TaskPriority.HIGH

    def test_create_task_minimal_fields(self):
        """Test creating schema with only required fields."""
        # Arrange & Act
        task = TaskCreate(title="Minimal Task")

        # Assert
        assert task.title == "Minimal Task"
        assert task.description is None
        assert task.status == TaskStatus.PENDING  # Default
        assert task.priority == TaskPriority.MEDIUM  # Default

    def test_create_task_title_stripped(self):
        """Test that title whitespace is stripped."""
        # Arrange & Act
        task = TaskCreate(title="  Trimmed Title  ")

        # Assert
        assert task.title == "Trimmed Title"

    def test_create_task_empty_title_raises_error(self):
        """Test that empty title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="")

        # Assert
        # Pydantic's min_length constraint catches empty string before custom validator
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_create_task_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="   ")

        # Assert
        assert "Title cannot be empty or whitespace" in str(exc_info.value)

    def test_create_task_missing_title_raises_error(self):
        """Test that missing title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate()

        # Assert
        assert "title" in str(exc_info.value).lower()

    @pytest.mark.parametrize("title_length", [1, 50, 100, 200])
    def test_create_task_title_length_valid(self, title_length):
        """Test valid title lengths."""
        # Arrange
        title = "A" * title_length

        # Act
        task = TaskCreate(title=title)

        # Assert
        assert len(task.title) == title_length

    def test_create_task_title_too_long_raises_error(self):
        """Test that title exceeding max length raises error."""
        # Arrange
        long_title = "A" * 201

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title=long_title)

        # Assert
        assert "String should have at most 200 characters" in str(exc_info.value)

    @pytest.mark.parametrize("description_length", [0, 100, 1000, 2000])
    def test_create_task_description_length_valid(self, description_length):
        """Test valid description lengths."""
        # Arrange
        description = "B" * description_length if description_length > 0 else None

        # Act
        task = TaskCreate(title="Test", description=description)

        # Assert
        if description:
            assert len(task.description) == description_length

    def test_create_task_description_too_long_raises_error(self):
        """Test that description exceeding max length raises error."""
        # Arrange
        long_description = "B" * 2001

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Test", description=long_description)

        # Assert
        assert "String should have at most 2000 characters" in str(exc_info.value)

    @pytest.mark.parametrize("status", [
        TaskStatus.PENDING,
        TaskStatus.IN_PROGRESS,
        TaskStatus.COMPLETED,
    ])
    def test_create_task_valid_statuses(self, status):
        """Test all valid status values."""
        # Arrange & Act
        task = TaskCreate(title="Test", status=status)

        # Assert
        assert task.status == status

    @pytest.mark.parametrize("priority", [
        TaskPriority.LOW,
        TaskPriority.MEDIUM,
        TaskPriority.HIGH,
    ])
    def test_create_task_valid_priorities(self, priority):
        """Test all valid priority values."""
        # Arrange & Act
        task = TaskCreate(title="Test", priority=priority)

        # Assert
        assert task.priority == priority

    def test_create_task_invalid_status_raises_error(self):
        """Test that invalid status value raises error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Test", status="invalid_status")

        # Assert
        assert "status" in str(exc_info.value).lower()

    def test_create_task_invalid_priority_raises_error(self):
        """Test that invalid priority value raises error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Test", priority="invalid_priority")

        # Assert
        assert "priority" in str(exc_info.value).lower()


@pytest.mark.unit
class TestTaskUpdate:
    """Test TaskUpdate schema validation."""

    def test_update_task_all_fields(self):
        """Test updating all fields."""
        # Arrange & Act
        update = TaskUpdate(
            title="Updated Title",
            description="Updated description",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.LOW
        )

        # Assert
        assert update.title == "Updated Title"
        assert update.description == "Updated description"
        assert update.status == TaskStatus.COMPLETED
        assert update.priority == TaskPriority.LOW

    def test_update_task_no_fields(self):
        """Test update with no fields (all None)."""
        # Arrange & Act
        update = TaskUpdate()

        # Assert
        assert update.title is None
        assert update.description is None
        assert update.status is None
        assert update.priority is None

    def test_update_task_partial_fields(self):
        """Test updating only specific fields."""
        # Arrange & Act
        update = TaskUpdate(title="Only Title")

        # Assert
        assert update.title == "Only Title"
        assert update.description is None
        assert update.status is None
        assert update.priority is None

    def test_update_task_title_stripped(self):
        """Test that title whitespace is stripped."""
        # Arrange & Act
        update = TaskUpdate(title="  Trimmed  ")

        # Assert
        assert update.title == "Trimmed"

    def test_update_task_empty_title_raises_error(self):
        """Test that empty title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(title="")

        # Assert
        # Pydantic's min_length constraint catches empty string before custom validator
        assert "String should have at least 1 character" in str(exc_info.value)

    def test_update_task_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(title="   ")

        # Assert
        assert "Title cannot be empty or whitespace" in str(exc_info.value)

    def test_update_task_title_too_long_raises_error(self):
        """Test that title exceeding max length raises error."""
        # Arrange
        long_title = "A" * 201

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(title=long_title)

        # Assert
        assert "String should have at most 200 characters" in str(exc_info.value)

    def test_update_task_description_too_long_raises_error(self):
        """Test that description exceeding max length raises error."""
        # Arrange
        long_description = "B" * 2001

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskUpdate(description=long_description)

        # Assert
        assert "String should have at most 2000 characters" in str(exc_info.value)

    @pytest.mark.parametrize("field,value", [
        ("title", "Updated Title"),
        ("description", "Updated Description"),
        ("status", TaskStatus.IN_PROGRESS),
        ("priority", TaskPriority.HIGH),
    ])
    def test_update_task_individual_fields(self, field, value):
        """Test updating individual fields."""
        # Arrange & Act
        update = TaskUpdate(**{field: value})

        # Assert
        assert getattr(update, field) == value


@pytest.mark.unit
class TestTaskResponse:
    """Test TaskResponse schema."""

    def test_response_schema_all_fields(self):
        """Test creating response schema with all fields."""
        # Arrange & Act
        response = TaskResponse(
            id=1,
            title="Response Task",
            description="Response description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            created_at=datetime(2024, 1, 10, 10, 0, 0),
            updated_at=datetime(2024, 1, 10, 14, 0, 0)
        )

        # Assert
        assert response.id == 1
        assert response.title == "Response Task"
        assert response.description == "Response description"
        assert response.status == TaskStatus.PENDING
        assert response.priority == TaskPriority.MEDIUM
        assert response.created_at == datetime(2024, 1, 10, 10, 0, 0)
        assert response.updated_at == datetime(2024, 1, 10, 14, 0, 0)

    def test_response_schema_missing_required_field_raises_error(self):
        """Test that missing required fields raise validation error."""
        # Arrange & Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            TaskResponse(
                title="Test",
                status=TaskStatus.PENDING,
                priority=TaskPriority.MEDIUM,
                # Missing id, created_at, updated_at
            )

        # Assert
        errors = str(exc_info.value)
        assert "id" in errors.lower() or "created_at" in errors.lower()


@pytest.mark.unit
class TestTaskListResponse:
    """Test TaskListResponse schema."""

    def test_list_response_schema_valid(self):
        """Test creating list response schema."""
        # Arrange
        task1 = TaskResponse(
            id=1,
            title="Task 1",
            status=TaskStatus.PENDING,
            priority=TaskPriority.LOW,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        task2 = TaskResponse(
            id=2,
            title="Task 2",
            status=TaskStatus.COMPLETED,
            priority=TaskPriority.HIGH,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Act
        response = TaskListResponse(
            items=[task1, task2],
            total=2,
            skip=0,
            limit=100
        )

        # Assert
        assert len(response.items) == 2
        assert response.total == 2
        assert response.skip == 0
        assert response.limit == 100

    def test_list_response_schema_empty_list(self):
        """Test list response with empty items."""
        # Arrange & Act
        response = TaskListResponse(
            items=[],
            total=0,
            skip=0,
            limit=100
        )

        # Assert
        assert len(response.items) == 0
        assert response.total == 0

    @pytest.mark.parametrize("skip,limit", [
        (0, 10),
        (10, 50),
        (100, 100),
    ])
    def test_list_response_pagination_values(self, skip, limit):
        """Test list response with various pagination values."""
        # Arrange & Act
        response = TaskListResponse(
            items=[],
            total=0,
            skip=skip,
            limit=limit
        )

        # Assert
        assert response.skip == skip
        assert response.limit == limit


@pytest.mark.unit
class TestSchemaEdgeCases:
    """Test edge cases and special characters in schemas."""

    @pytest.mark.parametrize("special_title", [
        "Task with emoji 🚀",
        "Task with Chinese 任务",
        "Task with Arabic العربية",
        "Task with <html>tags</html>",
        "Task with 'quotes' and \"double quotes\"",
        "Task\twith\ttabs",
        "Task\nwith\nnewlines",
    ])
    def test_create_task_special_characters(self, special_title):
        """Test tasks with special characters and Unicode."""
        # Arrange & Act
        task = TaskCreate(title=special_title)

        # Assert
        assert task.title is not None
        assert len(task.title) > 0

    def test_create_task_unicode_description(self):
        """Test description with Unicode characters."""
        # Arrange
        unicode_desc = "Description with emoji 📝 and symbols ©®™"

        # Act
        task = TaskCreate(title="Test", description=unicode_desc)

        # Assert
        assert task.description == unicode_desc

    @pytest.mark.parametrize("boundary_length", [1, 200])
    def test_create_task_boundary_title_lengths(self, boundary_length):
        """Test boundary values for title length."""
        # Arrange
        title = "T" * boundary_length

        # Act
        task = TaskCreate(title=title)

        # Assert
        assert len(task.title) == boundary_length

    @pytest.mark.parametrize("boundary_length", [1, 2000])
    def test_create_task_boundary_description_lengths(self, boundary_length):
        """Test boundary values for description length."""
        # Arrange
        description = "D" * boundary_length

        # Act
        task = TaskCreate(title="Test", description=description)

        # Assert
        assert len(task.description) == boundary_length
