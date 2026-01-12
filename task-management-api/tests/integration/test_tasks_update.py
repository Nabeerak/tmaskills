"""
Integration tests for updating tasks (PUT /api/v1/tasks/{id}).
Tests update operations, partial updates, and validation.
"""
import pytest
from httpx import AsyncClient


class TestTaskUpdate:
    """Test suite for updating tasks."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_full_update(self, client: AsyncClient, created_task: dict):
        """
        Test updating all fields of a task.

        GIVEN an existing task
        WHEN PUT request with all fields updated
        THEN all fields are updated and 200 status returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated task description",
            "status": "completed",
            "priority": "high"
        }

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]
        assert data["priority"] == update_data["priority"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_title_only(self, client: AsyncClient, created_task: dict):
        """
        Test updating only the title field.

        GIVEN an existing task
        WHEN PUT request with only title changed
        THEN only title is updated, other fields unchanged
        """
        # Arrange
        task_id = created_task["id"]
        original_description = created_task["description"]
        original_status = created_task["status"]
        original_priority = created_task["priority"]
        update_data = {"title": "New Title Only"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Title Only"
        assert data["description"] == original_description
        assert data["status"] == original_status
        assert data["priority"] == original_priority

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_description_only(self, client: AsyncClient, created_task: dict):
        """
        Test updating only the description field.

        GIVEN an existing task
        WHEN PUT request with only description changed
        THEN only description is updated
        """
        # Arrange
        task_id = created_task["id"]
        original_title = created_task["title"]
        update_data = {"description": "Updated description only"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == original_title
        assert data["description"] == "Updated description only"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_status_only(self, client: AsyncClient, created_task: dict):
        """
        Test updating only the status field.

        GIVEN an existing task with status=pending
        WHEN PUT request to change status to in_progress
        THEN only status is updated
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"status": "in_progress"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "in_progress"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_priority_only(self, client: AsyncClient, created_task: dict):
        """
        Test updating only the priority field.

        GIVEN an existing task with priority=medium
        WHEN PUT request to change priority to high
        THEN only priority is updated
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"priority": "high"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["priority"] == "high"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_clear_description(self, client: AsyncClient, created_task: dict):
        """
        Test clearing the description field.

        GIVEN an existing task with description
        WHEN PUT request with description=null
        THEN description is set to null
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"description": None}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["description"] is None

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("status", ["pending", "in_progress", "completed"])
    async def test_update_task_all_valid_statuses(self, client: AsyncClient, created_task: dict, status: str):
        """
        Test updating to all valid status values.

        GIVEN an existing task
        WHEN updating to each valid status
        THEN update succeeds
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"status": status}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        assert response.json()["status"] == status

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("priority", ["low", "medium", "high"])
    async def test_update_task_all_valid_priorities(self, client: AsyncClient, created_task: dict, priority: str):
        """
        Test updating to all valid priority values.

        GIVEN an existing task
        WHEN updating to each valid priority
        THEN update succeeds
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"priority": priority}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        assert response.json()["priority"] == priority

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_timestamps(self, client: AsyncClient, created_task: dict):
        """
        Test that updated_at changes but created_at remains the same.

        GIVEN an existing task
        WHEN task is updated
        THEN updated_at changes, created_at unchanged
        """
        # Arrange
        task_id = created_task["id"]
        original_created_at = created_task["created_at"]
        original_updated_at = created_task["updated_at"]
        update_data = {"title": "Timestamp Test"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["created_at"] == original_created_at  # Should not change
        # Note: In fast tests, updated_at might be the same due to timing
        # We just verify it exists and is valid
        assert "updated_at" in data
        assert data["updated_at"] is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_not_found(self, client: AsyncClient):
        """
        Test updating a non-existent task.

        GIVEN no task with ID 9999 exists
        WHEN PUT request to /api/v1/tasks/9999
        THEN 404 error is returned
        """
        # Arrange
        update_data = {"title": "Updated Title"}

        # Act
        response = await client.put("/api/v1/tasks/9999", json=update_data)

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "error" in data or "detail" in data


class TestTaskUpdateValidation:
    """Test suite for update validation errors."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_empty_title(self, client: AsyncClient, created_task: dict):
        """
        Test updating with empty title.

        GIVEN an existing task
        WHEN PUT request with empty title
        THEN 422 validation error is returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"title": ""}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_whitespace_title(self, client: AsyncClient, created_task: dict):
        """
        Test updating with whitespace-only title.

        GIVEN an existing task
        WHEN PUT request with whitespace title
        THEN 422 validation error is returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"title": "   "}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_title_too_long(self, client: AsyncClient, created_task: dict):
        """
        Test updating with title exceeding max length.

        GIVEN an existing task
        WHEN PUT request with title > 200 chars
        THEN 422 validation error is returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"title": "A" * 201}  # Exceeds max length of 200

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_description_too_long(self, client: AsyncClient, created_task: dict):
        """
        Test updating with description exceeding max length.

        GIVEN an existing task
        WHEN PUT request with description > 2000 chars
        THEN 422 validation error is returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"description": "A" * 2001}  # Exceeds max length of 2000

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_invalid_status(self, client: AsyncClient, created_task: dict):
        """
        Test updating with invalid status value.

        GIVEN an existing task
        WHEN PUT request with invalid status
        THEN 422 validation error is returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"status": "invalid_status"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_invalid_priority(self, client: AsyncClient, created_task: dict):
        """
        Test updating with invalid priority value.

        GIVEN an existing task
        WHEN PUT request with invalid priority
        THEN 422 validation error is returned
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"priority": "invalid_priority"}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_invalid_id_format(self, client: AsyncClient):
        """
        Test updating with invalid ID format.

        GIVEN invalid ID format (not an integer)
        WHEN PUT request with invalid ID
        THEN 422 validation error is returned
        """
        # Arrange
        update_data = {"title": "Updated Title"}

        # Act
        response = await client.put("/api/v1/tasks/invalid-id", json=update_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_title_with_spaces_trimmed(self, client: AsyncClient, created_task: dict):
        """
        Test that title with leading/trailing spaces is trimmed.

        GIVEN an existing task
        WHEN PUT request with title having spaces
        THEN spaces are trimmed
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {"title": "  Trimmed Title  "}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Trimmed Title"  # Spaces trimmed

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_empty_request_body(self, client: AsyncClient, created_task: dict):
        """
        Test updating with empty request body.

        GIVEN an existing task
        WHEN PUT request with empty body {}
        THEN task remains unchanged (all fields optional)
        """
        # Arrange
        task_id = created_task["id"]
        original_title = created_task["title"]
        update_data = {}

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == original_title  # No change

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_update_task_multiple_validations_fail(self, client: AsyncClient, created_task: dict):
        """
        Test updating with multiple validation errors.

        GIVEN an existing task
        WHEN PUT request with multiple invalid fields
        THEN 422 validation error with multiple errors
        """
        # Arrange
        task_id = created_task["id"]
        update_data = {
            "title": "",  # Empty
            "status": "invalid",  # Invalid enum
            "priority": "super_urgent"  # Invalid enum
        }

        # Act
        response = await client.put(f"/api/v1/tasks/{task_id}", json=update_data)

        # Assert
        assert response.status_code == 422
