"""
Integration tests for deleting tasks (DELETE /api/v1/tasks/{id}).
Tests task deletion and related error cases.
"""
import pytest
from httpx import AsyncClient


class TestTaskDeletion:
    """Test suite for deleting tasks."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_success(self, client: AsyncClient, created_task: dict):
        """
        Test successful task deletion.

        GIVEN an existing task
        WHEN DELETE request is made
        THEN 204 status is returned (no content)
        """
        # Arrange
        task_id = created_task["id"]

        # Act
        response = await client.delete(f"/api/v1/tasks/{task_id}")

        # Assert
        assert response.status_code == 204
        assert response.content == b""  # No content in response body

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_verify_deletion(self, client: AsyncClient, created_task: dict):
        """
        Test that deleted task is actually removed from database.

        GIVEN an existing task
        WHEN task is deleted
        THEN subsequent GET request returns 404
        """
        # Arrange
        task_id = created_task["id"]

        # Act
        delete_response = await client.delete(f"/api/v1/tasks/{task_id}")
        get_response = await client.get(f"/api/v1/tasks/{task_id}")

        # Assert
        assert delete_response.status_code == 204
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_not_in_list(self, client: AsyncClient, created_task: dict):
        """
        Test that deleted task doesn't appear in task list.

        GIVEN an existing task
        WHEN task is deleted
        THEN task list doesn't include the deleted task
        """
        # Arrange
        task_id = created_task["id"]

        # Act
        await client.delete(f"/api/v1/tasks/{task_id}")
        list_response = await client.get("/api/v1/tasks/")

        # Assert
        data = list_response.json()
        task_ids = [task["id"] for task in data["items"]]
        assert task_id not in task_ids
        assert data["total"] == 0  # Only one task existed, now deleted

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_not_found(self, client: AsyncClient):
        """
        Test deleting a non-existent task.

        GIVEN no task with ID 9999 exists
        WHEN DELETE request to /api/v1/tasks/9999
        THEN 404 error is returned
        """
        # Act
        response = await client.delete("/api/v1/tasks/9999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "error" in data or "detail" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_invalid_id_format(self, client: AsyncClient):
        """
        Test deleting with invalid ID format.

        GIVEN invalid ID format (not an integer)
        WHEN DELETE request with invalid ID
        THEN 422 validation error is returned
        """
        # Act
        response = await client.delete("/api/v1/tasks/invalid-id")

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_idempotency(self, client: AsyncClient, created_task: dict):
        """
        Test deleting the same task twice (not idempotent).

        GIVEN an existing task
        WHEN task is deleted twice
        THEN first deletion succeeds (204), second returns 404
        """
        # Arrange
        task_id = created_task["id"]

        # Act
        first_response = await client.delete(f"/api/v1/tasks/{task_id}")
        second_response = await client.delete(f"/api/v1/tasks/{task_id}")

        # Assert
        assert first_response.status_code == 204
        assert second_response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_doesnt_affect_others(self, client: AsyncClient, multiple_tasks: list):
        """
        Test that deleting one task doesn't affect other tasks.

        GIVEN multiple tasks exist
        WHEN one task is deleted
        THEN other tasks remain accessible
        """
        # Arrange
        task_to_delete = multiple_tasks[0]
        task_to_keep = multiple_tasks[1]

        # Act
        delete_response = await client.delete(f"/api/v1/tasks/{task_to_delete['id']}")
        get_response = await client.get(f"/api/v1/tasks/{task_to_keep['id']}")

        # Assert
        assert delete_response.status_code == 204
        assert get_response.status_code == 200
        assert get_response.json()["id"] == task_to_keep["id"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_updates_total_count(self, client: AsyncClient, multiple_tasks: list):
        """
        Test that deleting a task updates the total count.

        GIVEN 5 tasks exist
        WHEN 1 task is deleted
        THEN total count becomes 4
        """
        # Arrange
        initial_count = len(multiple_tasks)  # 5 tasks
        task_to_delete = multiple_tasks[0]

        # Act
        await client.delete(f"/api/v1/tasks/{task_to_delete['id']}")
        list_response = await client.get("/api/v1/tasks/")

        # Assert
        data = list_response.json()
        assert data["total"] == initial_count - 1  # 4 tasks remaining
        assert len(data["items"]) == initial_count - 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_all_tasks_sequentially(self, client: AsyncClient, multiple_tasks: list):
        """
        Test deleting all tasks one by one.

        GIVEN multiple tasks exist
        WHEN all tasks are deleted sequentially
        THEN final list is empty
        """
        # Act
        for task in multiple_tasks:
            response = await client.delete(f"/api/v1/tasks/{task['id']}")
            assert response.status_code == 204

        list_response = await client.get("/api/v1/tasks/")

        # Assert
        data = list_response.json()
        assert data["total"] == 0
        assert data["items"] == []

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_with_different_statuses(self, client: AsyncClient):
        """
        Test deleting tasks with different statuses.

        GIVEN tasks with various statuses
        WHEN each is deleted
        THEN all deletions succeed regardless of status
        """
        # Arrange - Create tasks with different statuses
        statuses = ["pending", "in_progress", "completed"]
        created_ids = []

        for status in statuses:
            response = await client.post(
                "/api/v1/tasks/",
                json={"title": f"Task {status}", "status": status}
            )
            created_ids.append(response.json()["id"])

        # Act & Assert
        for task_id in created_ids:
            response = await client.delete(f"/api/v1/tasks/{task_id}")
            assert response.status_code == 204

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_delete_task_cannot_update_after_deletion(self, client: AsyncClient, created_task: dict):
        """
        Test that deleted task cannot be updated.

        GIVEN a deleted task
        WHEN attempting to update it
        THEN 404 error is returned
        """
        # Arrange
        task_id = created_task["id"]
        await client.delete(f"/api/v1/tasks/{task_id}")

        # Act
        update_response = await client.put(
            f"/api/v1/tasks/{task_id}",
            json={"title": "Try to update deleted task"}
        )

        # Assert
        assert update_response.status_code == 404
