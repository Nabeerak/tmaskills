"""
Unit tests for Task CRUD operations.
Tests each CRUD function in isolation with mocked database sessions.
"""
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.task import (
    create_task,
    get_task,
    get_tasks,
    update_task,
    delete_task
)
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate


@pytest.mark.unit
class TestCreateTask:
    """Test create_task CRUD operation."""

    @pytest.mark.asyncio
    async def test_create_task_success(self):
        """Test successful task creation with all fields."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_data = TaskCreate(
            title="Test Task",
            description="Test Description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.HIGH
        )

        # Mock the session methods
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        # Act
        result = await create_task(mock_session, task_data)

        # Assert
        assert result.title == "Test Task"
        assert result.description == "Test Description"
        assert result.status == TaskStatus.PENDING
        assert result.priority == TaskPriority.HIGH
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_task_minimal_data(self):
        """Test task creation with only required fields."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_data = TaskCreate(title="Minimal Task")

        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        # Act
        result = await create_task(mock_session, task_data)

        # Assert
        assert result.title == "Minimal Task"
        assert result.status == TaskStatus.PENDING  # Default value
        assert result.priority == TaskPriority.MEDIUM  # Default value
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_task_with_defaults(self):
        """Test that default values are applied correctly."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_data = TaskCreate(title="Task with defaults")

        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        # Act
        result = await create_task(mock_session, task_data)

        # Assert
        assert result.status == TaskStatus.PENDING
        assert result.priority == TaskPriority.MEDIUM
        assert result.description is None


@pytest.mark.unit
class TestGetTask:
    """Test get_task CRUD operation."""

    @pytest.mark.asyncio
    async def test_get_task_found(self):
        """Test retrieving an existing task."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 1
        expected_task = Task(
            id=task_id,
            title="Found Task",
            description="Task description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM
        )

        # Mock the execute result
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = expected_task
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        result = await get_task(mock_session, task_id)

        # Assert
        assert result is not None
        assert result.id == task_id
        assert result.title == "Found Task"
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_task_not_found(self):
        """Test retrieving a non-existent task returns None."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 999

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        result = await get_task(mock_session, task_id)

        # Assert
        assert result is None
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("task_id", [0, -1, 1, 100, 999999])
    async def test_get_task_various_ids(self, task_id):
        """Test get_task with various valid and edge case IDs."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        result = await get_task(mock_session, task_id)

        # Assert
        mock_session.execute.assert_called_once()
        assert result is None  # All return None since we mock no task found


@pytest.mark.unit
class TestGetTasks:
    """Test get_tasks CRUD operation."""

    @pytest.mark.asyncio
    async def test_get_tasks_empty_database(self):
        """Test retrieving tasks from empty database."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)

        # Mock empty result for both queries
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        tasks, total = await get_tasks(mock_session)

        # Assert
        assert tasks == []
        assert total == 0
        assert mock_session.execute.call_count == 2  # Called twice: pagination + count

    @pytest.mark.asyncio
    async def test_get_tasks_with_results(self):
        """Test retrieving multiple tasks."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)

        task1 = Task(id=1, title="Task 1", status=TaskStatus.PENDING, priority=TaskPriority.LOW)
        task2 = Task(id=2, title="Task 2", status=TaskStatus.IN_PROGRESS, priority=TaskPriority.HIGH)
        task3 = Task(id=3, title="Task 3", status=TaskStatus.COMPLETED, priority=TaskPriority.MEDIUM)

        mock_tasks = [task1, task2, task3]

        # Mock pagination result
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_tasks
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        tasks, total = await get_tasks(mock_session, skip=0, limit=100)

        # Assert
        assert len(tasks) == 3
        assert total == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"

    @pytest.mark.asyncio
    @pytest.mark.parametrize("skip,limit", [
        (0, 10),
        (10, 10),
        (0, 100),
        (5, 20),
    ])
    async def test_get_tasks_pagination_parameters(self, skip, limit):
        """Test get_tasks with various pagination parameters."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_session.execute = AsyncMock(return_value=mock_result)

        # Act
        tasks, total = await get_tasks(mock_session, skip=skip, limit=limit)

        # Assert
        assert tasks == []
        assert total == 0
        mock_session.execute.assert_called()


@pytest.mark.unit
class TestUpdateTask:
    """Test update_task CRUD operation."""

    @pytest.mark.asyncio
    async def test_update_task_success(self):
        """Test successful task update."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 1

        existing_task = Task(
            id=task_id,
            title="Original Title",
            description="Original Description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.LOW,
            created_at=datetime(2024, 1, 1, 10, 0, 0),
            updated_at=datetime(2024, 1, 1, 10, 0, 0)
        )

        update_data = TaskUpdate(
            title="Updated Title",
            status=TaskStatus.IN_PROGRESS,
            priority=TaskPriority.HIGH
        )

        # Mock get_task to return existing task
        with patch('app.crud.task.get_task', return_value=existing_task):
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()

            # Act
            result = await update_task(mock_session, task_id, update_data)

            # Assert
            assert result is not None
            assert result.title == "Updated Title"
            assert result.status == TaskStatus.IN_PROGRESS
            assert result.priority == TaskPriority.HIGH
            assert result.description == "Original Description"  # Unchanged
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_task_not_found(self):
        """Test updating non-existent task returns None."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 999
        update_data = TaskUpdate(title="Updated Title")

        # Mock get_task to return None
        with patch('app.crud.task.get_task', return_value=None):
            # Act
            result = await update_task(mock_session, task_id, update_data)

            # Assert
            assert result is None

    @pytest.mark.asyncio
    async def test_update_task_partial_update(self):
        """Test updating only specific fields."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 1

        existing_task = Task(
            id=task_id,
            title="Original Title",
            description="Original Description",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM
        )

        # Update only status
        update_data = TaskUpdate(status=TaskStatus.COMPLETED)

        with patch('app.crud.task.get_task', return_value=existing_task):
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()

            # Act
            result = await update_task(mock_session, task_id, update_data)

            # Assert
            assert result.status == TaskStatus.COMPLETED
            assert result.title == "Original Title"  # Unchanged
            assert result.description == "Original Description"  # Unchanged
            assert result.priority == TaskPriority.MEDIUM  # Unchanged

    @pytest.mark.asyncio
    async def test_update_task_updates_timestamp(self):
        """Test that updated_at timestamp is modified."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 1

        old_timestamp = datetime(2024, 1, 1, 10, 0, 0)
        existing_task = Task(
            id=task_id,
            title="Original Title",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM,
            created_at=old_timestamp,
            updated_at=old_timestamp
        )

        update_data = TaskUpdate(title="Updated Title")

        with patch('app.crud.task.get_task', return_value=existing_task):
            mock_session.add = MagicMock()
            mock_session.commit = AsyncMock()
            mock_session.refresh = AsyncMock()

            # Act
            result = await update_task(mock_session, task_id, update_data)

            # Assert
            assert result.updated_at > old_timestamp


@pytest.mark.unit
class TestDeleteTask:
    """Test delete_task CRUD operation."""

    @pytest.mark.asyncio
    async def test_delete_task_success(self):
        """Test successful task deletion."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 1

        existing_task = Task(
            id=task_id,
            title="Task to Delete",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM
        )

        with patch('app.crud.task.get_task', return_value=existing_task):
            mock_session.delete = AsyncMock()
            mock_session.commit = AsyncMock()

            # Act
            result = await delete_task(mock_session, task_id)

            # Assert
            assert result is True
            mock_session.delete.assert_called_once_with(existing_task)
            mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self):
        """Test deleting non-existent task returns False."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)
        task_id = 999

        with patch('app.crud.task.get_task', return_value=None):
            # Act
            result = await delete_task(mock_session, task_id)

            # Assert
            assert result is False

    @pytest.mark.asyncio
    @pytest.mark.parametrize("task_id", [1, 100, 999])
    async def test_delete_task_various_ids(self, task_id):
        """Test delete operation with various task IDs."""
        # Arrange
        mock_session = AsyncMock(spec=AsyncSession)

        existing_task = Task(
            id=task_id,
            title=f"Task {task_id}",
            status=TaskStatus.PENDING,
            priority=TaskPriority.MEDIUM
        )

        with patch('app.crud.task.get_task', return_value=existing_task):
            mock_session.delete = AsyncMock()
            mock_session.commit = AsyncMock()

            # Act
            result = await delete_task(mock_session, task_id)

            # Assert
            assert result is True
            mock_session.delete.assert_called_once()
