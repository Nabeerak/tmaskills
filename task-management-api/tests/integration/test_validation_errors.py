"""
Integration tests for validation and error handling across all endpoints.
Tests edge cases, malformed requests, and error responses.
"""
import pytest
from httpx import AsyncClient


class TestRequestValidation:
    """Test suite for request validation and malformed data."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_missing_title(self, client: AsyncClient):
        """
        Test creating task without required title field.

        GIVEN request without title
        WHEN POST request is made
        THEN 422 validation error is returned
        """
        # Arrange
        task_data = {"description": "Task without title"}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_null_title(self, client: AsyncClient):
        """
        Test creating task with null title.

        GIVEN request with title=null
        WHEN POST request is made
        THEN 422 validation error is returned
        """
        # Arrange
        task_data = {"title": None}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_wrong_type_title(self, client: AsyncClient):
        """
        Test creating task with wrong type for title (integer instead of string).

        GIVEN title as integer
        WHEN POST request is made
        THEN 422 validation error is returned
        """
        # Arrange
        task_data = {"title": 12345}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        # Pydantic v2 may coerce to string, but if it fails, expect 422
        # If it succeeds, the title would be "12345" string
        if response.status_code == 201:
            # Type coercion succeeded
            assert response.json()["title"] == "12345"
        else:
            # Type validation failed
            assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_extra_fields_ignored(self, client: AsyncClient):
        """
        Test that extra fields in request are ignored.

        GIVEN request with extra fields not in schema
        WHEN POST request is made
        THEN task is created, extra fields ignored
        """
        # Arrange
        task_data = {
            "title": "Task with extra fields",
            "extra_field": "should be ignored",
            "another_extra": 123
        }

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "extra_field" not in data
        assert "another_extra" not in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_invalid_json(self, client: AsyncClient):
        """
        Test creating task with malformed JSON.

        GIVEN malformed JSON in request body
        WHEN POST request is made
        THEN 422 validation error is returned
        """
        # Act
        response = await client.post(
            "/api/v1/tasks/",
            content='{"title": "Invalid JSON"',  # Missing closing brace
            headers={"Content-Type": "application/json"}
        )

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_invalid_pagination_params(self, client: AsyncClient):
        """
        Test list tasks with invalid pagination parameters.

        GIVEN invalid skip/limit values
        WHEN GET request is made
        THEN 422 validation error is returned
        """
        # Act - negative skip
        response1 = await client.get("/api/v1/tasks/?skip=-1")
        # Act - negative limit
        response2 = await client.get("/api/v1/tasks/?limit=-1")

        # Assert
        assert response1.status_code == 422
        assert response2.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_tasks_non_integer_pagination(self, client: AsyncClient):
        """
        Test list tasks with non-integer pagination values.

        GIVEN non-integer skip/limit values
        WHEN GET request is made
        THEN 422 validation error is returned
        """
        # Act
        response1 = await client.get("/api/v1/tasks/?skip=abc")
        response2 = await client.get("/api/v1/tasks/?limit=xyz")

        # Assert
        assert response1.status_code == 422
        assert response2.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_tasks_invalid_status(self, client: AsyncClient):
        """
        Test filtering with invalid status value.

        GIVEN invalid status value
        WHEN GET request with status filter
        THEN 422 validation error is returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?status=invalid_status")

        # Assert
        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_filter_tasks_invalid_priority(self, client: AsyncClient):
        """
        Test filtering with invalid priority value.

        GIVEN invalid priority value
        WHEN GET request with priority filter
        THEN 422 validation error is returned
        """
        # Act
        response = await client.get("/api/v1/tasks/?priority=super_urgent")

        # Assert
        assert response.status_code == 422


class TestBoundaryValues:
    """Test suite for boundary value testing."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_title_exact_max_length(self, client: AsyncClient):
        """
        Test creating task with title at exact maximum length.

        GIVEN title with exactly 200 characters
        WHEN POST request is made
        THEN task is created successfully
        """
        # Arrange
        task_data = {"title": "A" * 200}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert len(response.json()["title"]) == 200

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_description_exact_max_length(self, client: AsyncClient):
        """
        Test creating task with description at exact maximum length.

        GIVEN description with exactly 2000 characters
        WHEN POST request is made
        THEN task is created successfully
        """
        # Arrange
        task_data = {
            "title": "Task with max description",
            "description": "B" * 2000
        }

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert len(response.json()["description"]) == 2000

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_title_one_char(self, client: AsyncClient):
        """
        Test creating task with minimum title length (1 character).

        GIVEN title with 1 character
        WHEN POST request is made
        THEN task is created successfully
        """
        # Arrange
        task_data = {"title": "A"}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        assert response.json()["title"] == "A"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_pagination_zero_limit(self, client: AsyncClient, multiple_tasks: list):
        """
        Test pagination with limit=0.

        GIVEN tasks exist
        WHEN GET request with limit=0
        THEN empty list returned (but total count available)
        """
        # Act
        response = await client.get("/api/v1/tasks/?limit=0")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 0
        assert data["total"] == 5  # Still shows total

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_pagination_very_large_limit(self, client: AsyncClient, multiple_tasks: list):
        """
        Test pagination with very large limit value.

        GIVEN 5 tasks exist
        WHEN GET request with limit=1000
        THEN all tasks returned (no error)
        """
        # Act
        response = await client.get("/api/v1/tasks/?limit=1000")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["tasks"]) == 5  # All tasks returned


class TestUnicodeAndSpecialCharacters:
    """Test suite for Unicode and special character handling."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    @pytest.mark.parametrize("special_title", [
        "Task with émojis 🚀🎉✨",
        "Task with Chinese 任务管理",
        "Task with Arabic مهمة",
        "Task with symbols !@#$%^&*()",
        "Task with quotes \"quoted\" 'text'",
        "Task with\ttabs\tand\nnewlines",
        "Task with backslash \\",
    ])
    async def test_create_task_special_characters(self, client: AsyncClient, special_title: str):
        """
        Test creating tasks with various special characters and Unicode.

        GIVEN titles with special characters
        WHEN tasks are created
        THEN tasks are created successfully
        """
        # Arrange
        task_data = {"title": special_title}

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        # Note: Some characters may be normalized or trimmed
        assert response.json()["title"] is not None

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_create_task_html_in_description(self, client: AsyncClient):
        """
        Test creating task with HTML in description.

        GIVEN description containing HTML tags
        WHEN task is created
        THEN HTML is stored as plain text (not executed)
        """
        # Arrange
        task_data = {
            "title": "Task with HTML",
            "description": "<script>alert('xss')</script><b>Bold text</b>"
        }

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 201
        # HTML should be stored as text, not executed
        assert "<script>" in response.json()["description"]


class TestErrorResponseFormat:
    """Test suite for consistent error response formats."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_404_error_has_consistent_format(self, client: AsyncClient):
        """
        Test that 404 errors return consistent format.

        GIVEN non-existent task
        WHEN GET request is made
        THEN error response has consistent structure
        """
        # Act
        response = await client.get("/api/v1/tasks/9999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        # Check for either FastAPI's default or custom error format
        assert "error" in data or "detail" in data

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_422_error_has_validation_details(self, client: AsyncClient):
        """
        Test that 422 errors include validation details.

        GIVEN invalid request data
        WHEN POST request is made
        THEN validation error includes details
        """
        # Arrange
        task_data = {"title": ""}  # Empty title

        # Act
        response = await client.post("/api/v1/tasks/", json=task_data)

        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        # FastAPI validation errors include location and message
        if isinstance(data["detail"], list):
            assert len(data["detail"]) > 0
            assert "loc" in data["detail"][0]
            assert "msg" in data["detail"][0]


class TestConcurrency:
    """Test suite for concurrent operations."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_concurrent_task_creation(self, client: AsyncClient):
        """
        Test creating multiple tasks concurrently.

        GIVEN multiple concurrent POST requests
        WHEN tasks are created simultaneously
        THEN all tasks get unique IDs
        """
        # Arrange
        import asyncio
        task_data_list = [
            {"title": f"Concurrent Task {i}"}
            for i in range(5)
        ]

        # Act - Create tasks concurrently
        responses = await asyncio.gather(*[
            client.post("/api/v1/tasks/", json=task_data)
            for task_data in task_data_list
        ])

        # Assert
        assert all(r.status_code == 201 for r in responses)
        task_ids = [r.json()["id"] for r in responses]
        # Verify unique IDs
        assert len(task_ids) == len(set(task_ids))

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_concurrent_updates_same_task(self, client: AsyncClient, created_task: dict):
        """
        Test concurrent updates to the same task.

        GIVEN one existing task
        WHEN multiple concurrent updates are made
        THEN one update wins (last write wins)
        """
        # Arrange
        import asyncio
        task_id = created_task["id"]
        update_data_list = [
            {"title": f"Updated Title {i}"}
            for i in range(3)
        ]

        # Act - Update task concurrently
        responses = await asyncio.gather(*[
            client.put(f"/api/v1/tasks/{task_id}", json=update_data)
            for update_data in update_data_list
        ])

        # Assert
        assert all(r.status_code == 200 for r in responses)

        # Get final state
        final_response = await client.get(f"/api/v1/tasks/{task_id}")
        assert final_response.status_code == 200
        # One of the titles should have won
        final_title = final_response.json()["title"]
        assert final_title.startswith("Updated Title")
