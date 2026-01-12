"""
Integration tests for task creation (POST /api/v1/tasks/).
Tests the complete flow of creating tasks with validation.
"""
import pytest
from httpx import AsyncClient


class TestTaskCreation:
    """Test suite for creating tasks."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_success(self, client: AsyncClient, sample_task_data: dict):
        """
        Test successful task creation with valid data.
        
        GIVEN valid task data
        WHEN POST request is made to /api/v1/tasks/
        THEN task is created and returned with 201 status
        """
        # Arrange
        task_data = sample_task_data

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert data["priority"] == task_data["priority"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_with_minimal_data(self, client: AsyncClient):
        """
        Test task creation with only required fields.
        
        GIVEN task data with only title (required field)
        WHEN POST request is made
        THEN task is created with default values
        """
        # Arrange
        minimal_data = {"title": "Minimal Task"}

        # Act
        response = await client.post("/api/v1/tasks/", json=minimal_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["description"] is None
        assert data["status"] == "pending"  # Default value
        assert data["priority"] == "medium"  # Default value

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("title,expected_title", [
        ("Simple Task", "Simple Task"),
        ("  Task with spaces  ", "Task with spaces"),  # Tests trimming
        ("Task with special chars !@#$%", "Task with special chars !@#$%"),
        ("Task with Unicode 你好🚀", "Task with Unicode 你好🚀"),
        ("A" * 200, "A" * 200),  # Max length (200 chars)
    ])
    async def test_create_task_title_variations(
        self, client: AsyncClient, title: str, expected_title: str
    ):
        """
        Test task creation with various valid title formats.
        
        GIVEN different valid title formats
        WHEN tasks are created
        THEN titles are stored correctly
        """
        # Arrange
        task_data = {"title": title}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["title"] == expected_title

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("status", ["pending", "in_progress", "completed"])
    async def test_create_task_all_valid_statuses(self, client: AsyncClient, status: str):
        """
        Test task creation with all valid status values.
        
        GIVEN all possible valid status values
        WHEN tasks are created with each status
        THEN tasks are created successfully
        """
        # Arrange
        task_data = {"title": f"Task with {status} status", "status": status}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["status"] == status

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("priority", ["low", "medium", "high"])
    async def test_create_task_all_valid_priorities(self, client: AsyncClient, priority: str):
        """
        Test task creation with all valid priority values.
        
        GIVEN all possible valid priority values
        WHEN tasks are created with each priority
        THEN tasks are created successfully
        """
        # Arrange
        task_data = {"title": f"Task with {priority} priority", "priority": priority}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["priority"] == priority

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_with_long_description(self, client: AsyncClient):
        """
        Test task creation with maximum allowed description length.
        
        GIVEN description at max length (2000 chars)
        WHEN task is created
        THEN task is created successfully
        """
        # Arrange
        long_description = "A" * 2000  # Max length
        task_data = {
            "title": "Task with long description",
            "description": long_description
        }

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["description"] == long_description
        assert len(response.json()["description"]) == 2000

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_multiple_tasks(self, client: AsyncClient):
        """
        Test creating multiple tasks sequentially.
        
        GIVEN multiple task creation requests
        WHEN tasks are created one after another
        THEN each task gets a unique ID
        """
        # Arrange
        task1_data = {"title": "First Task"}
        task2_data = {"title": "Second Task"}
        task3_data = {"title": "Third Task"}

        # Act
        response1 = await client.post("/api/v1/tasks/", json=task1_data)
        response2 = await client.post("/api/v1/tasks/", json=task2_data)
        response3 = await client.post("/api/v1/tasks/", json=task3_data)

        # Assert
        assert response1.status_code == 201
        assert response2.status_code == 201
        assert response3.status_code == 201

        task1 = response1.json()
        task2 = response2.json()
        task3 = response3.json()

        # Verify unique IDs
        assert task1["id"] != task2["id"]
        assert task2["id"] != task3["id"]
        assert task1["id"] != task3["id"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_timestamps(self, client: AsyncClient):
        """
        Test that created_at and updated_at timestamps are set.
        
        GIVEN a new task
        WHEN task is created
        THEN created_at and updated_at are set and equal
        """
        # Arrange
        task_data = {"title": "Timestamp Test Task"}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data
        assert data["created_at"] is not None
        assert data["updated_at"] is not None
        # For newly created tasks, timestamps should be the same
        assert data["created_at"] == data["updated_at"]
