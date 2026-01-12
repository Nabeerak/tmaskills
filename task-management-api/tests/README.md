# Task Management API - Test Suite

Comprehensive integration tests for the Task Management API built with FastAPI and SQLModel.

## Test Structure

```
tests/
├── conftest.py                           # Shared fixtures and configuration
├── integration/
│   ├── test_tasks_create.py             # POST endpoint tests (10 tests)
│   ├── test_tasks_read.py               # GET endpoints tests (19 tests)
│   ├── test_tasks_update.py             # PUT endpoint tests (22 tests)
│   ├── test_tasks_delete.py             # DELETE endpoint tests (12 tests)
│   └── test_validation_errors.py        # Validation & error handling (23 tests)
└── README.md                             # This file
```

**Total: 86 test cases**

## Test Coverage

### CRUD Operations
- ✅ **Create Tasks** (POST /api/v1/tasks/)
  - Valid task creation with all fields
  - Minimal data with defaults
  - Title variations (spaces, Unicode, special chars)
  - All status values (pending, in_progress, completed)
  - All priority values (low, medium, high)
  - Boundary testing (max lengths)

- ✅ **Read Tasks** (GET /api/v1/tasks/ and /api/v1/tasks/{id})
  - List all tasks with pagination (skip, limit)
  - Filter by status and priority
  - Combined filtering
  - Empty results handling
  - Get single task by ID
  - 404 for non-existent tasks

- ✅ **Update Tasks** (PUT /api/v1/tasks/{id})
  - Full updates (all fields)
  - Partial updates (individual fields)
  - Timestamp behavior (updated_at changes)
  - Validation errors (empty title, too long)
  - 404 for non-existent tasks

- ✅ **Delete Tasks** (DELETE /api/v1/tasks/{id})
  - Successful deletion (204 status)
  - Verification that task is removed
  - Idempotency testing
  - Doesn't affect other tasks

### Validation & Error Handling
- ✅ Request validation (missing fields, wrong types, malformed JSON)
- ✅ Boundary value testing (min/max lengths, edge cases)
- ✅ Unicode and special characters (emojis, Chinese, Arabic, HTML)
- ✅ Pagination parameter validation
- ✅ Filter parameter validation
- ✅ Consistent error response formats (404, 422)
- ✅ Concurrency testing (concurrent creates/updates)

## Running Tests

### Prerequisites

Install dependencies:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run All Tests

```bash
# Run all tests with verbose output
pytest -v tests/

# Run all tests with coverage
pytest -v --cov=app --cov-report=html --cov-report=term-missing tests/

# Run specific test file
pytest -v tests/integration/test_tasks_create.py

# Run specific test class
pytest -v tests/integration/test_tasks_read.py::TestTaskFiltering

# Run specific test method
pytest -v tests/integration/test_tasks_create.py::TestTaskCreation::test_create_task_success
```

### Run Tests by Marker

```bash
# Run only integration tests
pytest -v -m integration tests/

# Run only unit tests (when added)
pytest -v -m unit tests/

# Exclude slow tests
pytest -v -m "not slow" tests/
```

### Coverage Report

After running tests with `--cov`, view the HTML report:
```bash
# Open coverage report in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Test Fixtures

### Database Fixtures
- **`test_engine`**: Creates in-memory SQLite database with tables
- **`test_session`**: Provides database session with automatic rollback
- **`client`**: AsyncClient for making API requests

### Data Fixtures
- **`sample_task_data`**: Standard task data for testing
- **`sample_task_update_data`**: Update data for testing
- **`created_task`**: Creates a task and returns its data
- **`multiple_tasks`**: Creates 5 tasks with different statuses/priorities

## Test Patterns

All tests follow the **AAA pattern**:
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code being tested
- **Assert**: Verify the expected outcome

Example:
```python
async def test_create_task_success(self, client: AsyncClient, sample_task_data: dict):
    # Arrange
    task_data = sample_task_data

    # Act
    response = await client.post("/api/v1/tasks/", json=task_data)

    # Assert
    assert response.status_code == 201
    assert response.json()["title"] == task_data["title"]
```

## Test Database

Tests use an **in-memory SQLite database** for:
- ✅ Fast execution (no disk I/O)
- ✅ Isolation (each test gets fresh database)
- ✅ No cleanup required (database destroyed after test)

Configuration in `conftest.py`:
```python
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
```

## Expected Coverage

Target: **80%+ code coverage** on critical paths

Coverage includes:
- All CRUD operations (app/crud/)
- All API endpoints (app/api/)
- Request/response schemas (app/schemas/)
- Database models (app/models/)
- Exception handlers (app/exceptions/)

## Troubleshooting

### Tests Failing with Database Errors

Ensure tables are created:
```python
# In conftest.py, test_engine fixture creates tables:
async with engine.begin() as conn:
    await conn.run_sync(SQLModel.metadata.create_all)
```

### Tests Timing Out

Increase timeout in pytest.ini:
```ini
[pytest]
asyncio_mode = auto
timeout = 30  # seconds
```

### Import Errors

Ensure app module is in Python path:
```bash
# Run from project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/
```

## Continuous Integration

For CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml --cov-report=term tests/

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Future Enhancements

Potential additions to the test suite:
- [ ] Unit tests for individual functions (app/crud/, app/core/)
- [ ] Performance tests for pagination with large datasets
- [ ] Stress tests for concurrent operations
- [ ] API endpoint security tests (OWASP Top 10)
- [ ] Integration tests with real PostgreSQL database

## References

- **Pytest Documentation**: https://docs.pytest.org/
- **pytest-asyncio**: https://pytest-asyncio.readthedocs.io/
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **SQLModel Testing**: https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/
- **httpx AsyncClient**: https://www.python-httpx.org/async/

---

**Test Suite Version**: 1.0.0
**Created**: 2026-01-11
**Framework**: pytest 8.0.0 + pytest-asyncio 0.23.3
**Coverage Target**: 80%+
