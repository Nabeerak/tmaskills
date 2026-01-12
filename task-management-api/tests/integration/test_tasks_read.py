"""
Integration tests for reading tasks (GET /api/v1/tasks/ and GET /api/v1/tasks/{id}).
Tests retrieval, pagination, and filtering functionality.
"""
import pytest
from httpx import AsyncClient


class TestTaskRetrievalList:
    """Test suite for listing tasks (GET /api/v1/tasks/)."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_empty_list(self, client: AsyncClient):
        """
        Test retrieving tasks when database is empty.

        GIVEN no tasks in database
        WHEN GET request is made to /api/v1/tasks/
        THEN empty list is returned with 200 status
        """
        # Act
        response = await client.get("/api/v1/tasks/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "tasks" in data
        assert "total" in data
        assert data["tasks"] == []
        assert data["total"] == 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_single_task(self, client: AsyncClient, created_task: dict):
        """
        Test retrieving tasks with a single task in database.

        GIVEN one task exists
        WHEN GET request is made
        THEN single task is returned in list
        """
        # Act
        response = await client.get("/api/v1/tasks/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1
        assert data["total"] == 1
        assert data["tasks"][0]["id"] == created_task["id"]
        assert data["tasks"][0]["title"] == created_task["title"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_multiple_tasks(self, client: AsyncClient, multiple_tasks: list):
        """
        Test retrieving multiple tasks.

        GIVEN multiple tasks exist
        WHEN GET request is made
        THEN all tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 5  # multiple_tasks fixture creates 5 tasks
        assert data["total"] == 5

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_with_pagination(self, client: AsyncClient, multiple_tasks: list):
        """
        Test pagination with skip and limit parameters.

        GIVEN 5 tasks exist
        WHEN request with skip=2, limit=2
        THEN only 2 tasks are returned (items 3 and 4)
        """
        # Act
        response = await client.get("/api/v1/tasks/?skip=2&limit=2")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 2
        assert data["total"] == 5  # Total count remains 5
        # Verify we got the 3rd and 4th tasks (0-indexed: items 2 and 3)
        assert data["tasks"][0]["title"] == "Task 3"
        assert data["tasks"][1]["title"] == "Task 4"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_pagination_limit_only(self, client: AsyncClient, multiple_tasks: list):
        """
        Test pagination with limit parameter only.

        GIVEN 5 tasks exist
        WHEN request with limit=3
        THEN first 3 tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?limit=3")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 3
        assert data["total"] == 5

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_pagination_skip_beyond_total(self, client: AsyncClient, multiple_tasks: list):
        """
        Test pagination when skip exceeds total count.

        GIVEN 5 tasks exist
        WHEN request with skip=10
        THEN empty list is returned but total shows 5
        """
        # Act
        response = await client.get("/api/v1/tasks/?skip=10")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 0
        assert data["total"] == 5  # Total count unchanged


class TestTaskFiltering:
    """Test suite for filtering tasks by status and priority."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_status_pending(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering tasks by status=pending.

        GIVEN tasks with different statuses
        WHEN filtering by status=pending
        THEN only pending tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?status=pending")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 2 pending tasks (Task 1, Task 4)
        assert len(data["tasks"]) == 2
        assert data["total"] == 2
        for task in data["tasks"]:
            assert task["status"] == "pending"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_status_in_progress(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering tasks by status=in_progress.

        GIVEN tasks with different statuses
        WHEN filtering by status=in_progress
        THEN only in_progress tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?status=in_progress")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 2 in_progress tasks (Task 2, Task 5)
        assert len(data["tasks"]) == 2
        assert data["total"] == 2
        for task in data["tasks"]:
            assert task["status"] == "in_progress"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_status_completed(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering tasks by status=completed.

        GIVEN tasks with different statuses
        WHEN filtering by status=completed
        THEN only completed tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?status=completed")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 1 completed task (Task 3)
        assert len(data["tasks"]) == 1
        assert data["total"] == 1
        assert data["tasks"][0]["status"] == "completed"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_priority_low(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering tasks by priority=low.

        GIVEN tasks with different priorities
        WHEN filtering by priority=low
        THEN only low priority tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?priority=low")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 2 low priority tasks (Task 1, Task 5)
        assert len(data["tasks"]) == 2
        assert data["total"] == 2
        for task in data["tasks"]:
            assert task["priority"] == "low"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_priority_medium(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering tasks by priority=medium.

        GIVEN tasks with different priorities
        WHEN filtering by priority=medium
        THEN only medium priority tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?priority=medium")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 1 medium priority task (Task 2)
        assert len(data["tasks"]) == 1
        assert data["total"] == 1
        assert data["tasks"][0]["priority"] == "medium"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_priority_high(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering tasks by priority=high.

        GIVEN tasks with different priorities
        WHEN filtering by priority=high
        THEN only high priority tasks are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?priority=high")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 2 high priority tasks (Task 3, Task 4)
        assert len(data["tasks"]) == 2
        assert data["total"] == 2
        for task in data["tasks"]:
            assert task["priority"] == "high"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_by_status_and_priority(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering by both status and priority.

        GIVEN tasks with various status/priority combinations
        WHEN filtering by status=pending AND priority=high
        THEN only tasks matching both criteria are returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?status=pending&priority=high")

        # Assert
        assert response.status_code == 200
        data = response.json()
        # multiple_tasks has 1 task with pending + high (Task 4)
        assert len(data["tasks"]) == 1
        assert data["total"] == 1
        assert data["tasks"][0]["status"] == "pending"
        assert data["tasks"][0]["priority"] == "high"
        assert data["tasks"][0]["title"] == "Task 4"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_no_matches(self, client: AsyncClient, multiple_tasks: list):
        """
        Test filtering with criteria that match no tasks.

        GIVEN tasks in database
        WHEN filtering by status=completed AND priority=low (no match)
        THEN empty list is returned
        """
        # Act (Task 3 is completed+high, not completed+low)
        response = await client.get("/api/v1/tasks/?status=completed&priority=low")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 0
        assert data["total"] == 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_with_pagination(self, client: AsyncClient, multiple_tasks: list):
        """
        Test combining filtering with pagination.

        GIVEN tasks with different priorities
        WHEN filtering by priority=high with limit=1
        THEN only 1 high priority task returned, total shows 2
        """
        # Act
        response = await client.get("/api/v1/tasks/?priority=high&limit=1")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 1  # Limited to 1
        assert data["total"] == 2  # But 2 high priority tasks exist
        assert data["tasks"][0]["priority"] == "high"


class TestTaskRetrievalSingle:
    """Test suite for retrieving a single task (GET /api/v1/tasks/{id})."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_task_by_id_success(self, client: AsyncClient, created_task: dict):
        """
        Test retrieving a specific task by ID.

        GIVEN a task exists with specific ID
        WHEN GET request to /api/v1/tasks/{id}
        THEN task details are returned with 200 status
        """
        # Arrange
        task_id = created_task["id"]

        # Act
        response = await client.get(f"/api/v1/tasks/{task_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == created_task["title"]
        assert data["description"] == created_task["description"]
        assert data["status"] == created_task["status"]
        assert data["priority"] == created_task["priority"]
        assert "created_at" in data
        assert "updated_at" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_task_by_id_not_found(self, client: AsyncClient):
        """
        Test retrieving a non-existent task.

        GIVEN no task with ID 9999 exists
        WHEN GET request to /api/v1/tasks/9999
        THEN 404 error is returned
        """
        # Act
        response = await client.get("/api/v1/tasks/9999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "error" in data or "detail" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_task_by_id_invalid_id_format(self, client: AsyncClient):
        """
        Test retrieving task with invalid ID format.

        GIVEN invalid ID format (not an integer)
        WHEN GET request with invalid ID
        THEN 422 validation error is returned
        """
        # Act
        response = await client.get("/api/v1/tasks/invalid-id")

        # Assert
        assert response.status_code == 422  # Validation error

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_task_verify_all_fields(self, client: AsyncClient):
        """
        Test that retrieved task contains all expected fields.

        GIVEN a task with all fields populated
        WHEN task is retrieved
        THEN all fields are present in response
        """
        # Arrange - Create task with all fields
        task_data = {
            "title": "Complete Task",
            "description": "Task with all fields",
            "status": "in_progress",
            "priority": "high"
        }
        create_response = await client.post("/api/v1/tasks/", json=task_data)
        task_id = create_response.json()["id"]

        # Act
        response = await client.get(f"/api/v1/tasks/{task_id}")

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Verify all required fields present
        required_fields = ["id", "title", "description", "status", "priority", "created_at", "updated_at"]
        for field in required_fields:
            assert field in data, f"Field '{field}' missing from response"

        # Verify values match
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert data["priority"] == task_data["priority"]
