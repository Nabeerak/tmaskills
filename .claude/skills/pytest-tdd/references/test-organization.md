# Test Organization and Structure

## Table of Contents

- [Project Structure](#project-structure)
- [Test Directory Layout](#test-directory-layout)
- [conftest.py Usage](#conftestpy-usage)
- [Organizing Tests by Type](#organizing-tests-by-type)
- [Test Naming Conventions](#test-naming-conventions)
- [Test Discovery](#test-discovery)
- [Best Practices](#best-practices)

---

## Project Structure

Mirror your production code structure in tests for easy navigation.

### Standard Layout

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── product.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── user_service.py
│       │   └── product_service.py
│       └── api/
│           ├── __init__.py
│           └── routes.py
├── tests/
│   ├── conftest.py              # Root fixtures
│   ├── unit/
│   │   ├── conftest.py          # Unit test fixtures
│   │   ├── models/
│   │   │   ├── test_user.py
│   │   │   └── test_product.py
│   │   └── services/
│   │       ├── test_user_service.py
│       └── test_product_service.py
│   ├── integration/
│   │   ├── conftest.py          # Integration test fixtures
│   │   ├── test_api.py
│   │   └── test_database.py
│   ├── functional/
│   │   ├── conftest.py
│   │   └── test_user_workflows.py
│   └── fixtures/
│       ├── __init__.py
│       ├── users.py             # User test data
│       └── products.py          # Product test data
├── pytest.ini                   # Pytest configuration
├── pyproject.toml              # Modern configuration
└── .coveragerc                 # Coverage configuration
```

### Flat Layout (Small Projects)

```
project/
├── myapp/
│   ├── __init__.py
│   ├── models.py
│   ├── services.py
│   └── api.py
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_api.py
└── pytest.ini
```

---

## Test Directory Layout

### Unit Tests

Tests for individual functions/classes in isolation.

```
tests/unit/
├── conftest.py
├── test_calculator.py           # Tests for calculator.py
├── test_validators.py           # Tests for validators.py
└── models/
    ├── test_user.py
    └── test_product.py
```

### Integration Tests

Tests for interactions between components.

```
tests/integration/
├── conftest.py                  # Database fixtures, API clients
├── test_api_endpoints.py        # API integration tests
├── test_database_operations.py  # Database integration tests
└── test_external_services.py    # External API integration tests
```

### Functional/E2E Tests

Tests for complete user workflows.

```
tests/functional/
├── conftest.py
├── test_user_registration.py    # Complete registration flow
├── test_checkout_process.py     # End-to-end checkout
└── test_admin_workflows.py      # Admin user workflows
```

---

## conftest.py Usage

`conftest.py` files define fixtures available to all tests in that directory and subdirectories.

### Root conftest.py

Share fixtures across all tests:

```python
# tests/conftest.py
import pytest
from myapp import create_app
from myapp.database import init_db

@pytest.fixture(scope="session")
def app():
    """Create application for testing."""
    app = create_app(testing=True)
    return app

@pytest.fixture(scope="session")
def db():
    """Create database for testing."""
    database = init_db(":memory:")
    yield database
    database.close()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()
```

### Unit Test conftest.py

Fixtures specific to unit tests:

```python
# tests/unit/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_database():
    """Mock database for unit tests."""
    return Mock()

@pytest.fixture
def sample_user_data():
    """Sample user data for unit tests."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
```

### Integration Test conftest.py

Fixtures for integration tests:

```python
# tests/integration/conftest.py
import pytest
from sqlmodel import Session, create_engine, SQLModel
from myapp.database import get_session

@pytest.fixture(scope="function")
def db_session():
    """Provide database session with automatic rollback."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

@pytest.fixture
def authenticated_client(client, db_session):
    """Provide client with authentication."""
    # Create test user
    user = create_test_user(db_session)

    # Get auth token
    token = create_access_token(user.id)

    # Add token to client headers
    client.headers = {"Authorization": f"Bearer {token}"}

    return client
```

### Hierarchical Fixtures

Fixtures can depend on fixtures from parent conftest.py files:

```
tests/
├── conftest.py                  # app, db (scope: session)
├── unit/
│   ├── conftest.py              # mock_db (scope: function)
│   └── test_user.py             # Can use: app, db, mock_db
└── integration/
    ├── conftest.py              # db_session (scope: function)
    └── test_api.py              # Can use: app, db, db_session
```

---

## Organizing Tests by Type

### By Test Type (Recommended)

Organize by unit/integration/functional:

```
tests/
├── unit/           # Fast, isolated tests
├── integration/    # Tests with real dependencies
└── functional/     # End-to-end tests
```

**Run specific types**:
```bash
pytest tests/unit              # Only unit tests
pytest tests/integration       # Only integration tests
pytest -m "not slow"           # Exclude slow tests
```

### By Module

Mirror production code structure:

```
tests/
├── models/
│   ├── test_user.py
│   └── test_product.py
├── services/
│   ├── test_user_service.py
│   └── test_product_service.py
└── api/
    └── test_routes.py
```

**When to use**: Small projects, clear module boundaries.

### By Feature

Organize by business features:

```
tests/
├── user_management/
│   ├── test_registration.py
│   ├── test_authentication.py
│   └── test_profile.py
├── shopping_cart/
│   ├── test_add_items.py
│   ├── test_checkout.py
│   └── test_payment.py
```

**When to use**: Feature-driven development, microservices.

---

## Test Naming Conventions

### File Names

- Prefix with `test_`: `test_calculator.py`
- Mirror production files: `calculator.py` → `test_calculator.py`
- Descriptive names: `test_user_authentication.py`

### Test Function Names

Follow pattern: `test_<what>_<condition>_<expected_result>`

```python
# ✓ Good names
def test_add_positive_numbers_returns_sum():
    ...

def test_divide_by_zero_raises_error():
    ...

def test_user_registration_with_valid_data_creates_user():
    ...

def test_user_registration_with_duplicate_email_fails():
    ...

# ❌ Bad names
def test_add():
    ...

def test_user():
    ...

def test_error():
    ...
```

### Test Class Names

- Prefix with `Test`: `class TestCalculator:`
- Group related tests: `class TestUserAuthentication:`

```python
class TestCalculator:
    """Tests for Calculator class."""

    def test_add_returns_sum(self):
        ...

    def test_subtract_returns_difference(self):
        ...

class TestUserAuthentication:
    """Tests for user authentication."""

    def test_login_with_valid_credentials_succeeds(self):
        ...

    def test_login_with_invalid_credentials_fails(self):
        ...
```

---

## Test Discovery

Pytest automatically discovers tests following these conventions:

### Default Discovery Rules

- Files: `test_*.py` or `*_test.py`
- Classes: `Test*` (no `__init__` method)
- Functions: `test_*`

### Configure Discovery

```ini
# pytest.ini
[pytest]
python_files = test_*.py *_test.py
python_classes = Test* *Tests
python_functions = test_* check_*
testpaths = tests
```

### Custom Discovery

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests", "integration_tests"]
python_files = ["test_*.py", "*_test.py", "check_*.py"]
python_classes = ["Test*", "Verify*"]
python_functions = ["test_*", "verify_*"]
```

---

## Best Practices

### 1. Mirror Production Structure

Tests should mirror production code for easy navigation:

```
src/myapp/models/user.py  →  tests/unit/models/test_user.py
src/myapp/api/routes.py   →  tests/integration/test_routes.py
```

### 2. Separate Test Types

Keep unit, integration, and functional tests separate:

```bash
# Run only fast unit tests during development
pytest tests/unit

# Run all tests before committing
pytest

# Run slow tests in CI/CD
pytest tests/integration tests/functional
```

### 3. Use conftest.py Hierarchically

- **Root conftest.py**: Application-wide fixtures (app, db)
- **Directory conftest.py**: Type-specific fixtures (mock_db for unit, db_session for integration)
- **Module-level**: Use `@pytest.fixture` in test file for test-specific fixtures

### 4. Keep Test Data Separate

```
tests/fixtures/
├── users.py              # User test data
├── products.py           # Product test data
└── api_responses.py      # Mock API responses
```

```python
# tests/fixtures/users.py
def get_sample_user():
    return {
        "name": "John Doe",
        "email": "john@example.com"
    }

def get_admin_user():
    return {
        "name": "Admin",
        "email": "admin@example.com",
        "role": "admin"
    }

# tests/unit/test_user.py
from tests.fixtures.users import get_sample_user

def test_user_creation():
    user_data = get_sample_user()
    user = User(**user_data)
    assert user.name == "John Doe"
```

### 5. Use Markers for Organization

```python
import pytest

@pytest.mark.unit
def test_add():
    ...

@pytest.mark.integration
def test_database_query():
    ...

@pytest.mark.slow
def test_large_file_processing():
    ...
```

**pytest.ini**:
```ini
[pytest]
markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (with dependencies)
    slow: Slow running tests
    smoke: Smoke tests (critical functionality)
```

**Run by marker**:
```bash
pytest -m unit                # Only unit tests
pytest -m "not slow"          # Exclude slow tests
pytest -m "unit or integration"  # Union
```

### 6. Clean Test Output

Use descriptive docstrings:

```python
def test_user_registration_sends_welcome_email():
    """
    Test that registering a new user sends a welcome email.

    Given a new user registration
    When the user is created
    Then a welcome email should be sent to the user's email address
    """
    ...
```

**Output**:
```
tests/test_user.py::test_user_registration_sends_welcome_email PASSED
    Test that registering a new user sends a welcome email.
```

### 7. Avoid Deep Nesting

```
# ✓ Good - Flat structure
tests/
├── unit/
│   ├── test_user.py
│   └── test_product.py

# ❌ Bad - Too deep
tests/
└── unit/
    └── models/
        └── user/
            └── validation/
                └── test_email.py
```

---

## Example: Complete Organization

### Project Structure

```
ecommerce/
├── src/
│   └── ecommerce/
│       ├── __init__.py
│       ├── models/
│       │   ├── user.py
│       │   └── product.py
│       ├── services/
│       │   ├── user_service.py
│       │   └── cart_service.py
│       └── api/
│           └── routes.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── conftest.py
│   │   ├── models/
│   │   │   ├── test_user.py
│   │   │   └── test_product.py
│   │   └── services/
│   │       ├── test_user_service.py
│   │       └── test_cart_service.py
│   ├── integration/
│   │   ├── conftest.py
│   │   ├── test_api_routes.py
│   │   └── test_database.py
│   ├── functional/
│   │   ├── conftest.py
│   │   └── test_checkout_flow.py
│   └── fixtures/
│       ├── users.py
│       └── products.py
├── pytest.ini
└── pyproject.toml
```

### pytest.ini Configuration

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Output
addopts =
    -v
    --strict-markers
    --cov=ecommerce
    --cov-report=html
    --cov-report=term-missing

# Markers
markers =
    unit: Unit tests
    integration: Integration tests
    functional: Functional/E2E tests
    slow: Slow running tests
    smoke: Smoke tests

# Coverage
[coverage:run]
source = ecommerce
omit = */tests/*, */migrations/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
```

---

## Summary

**Key Principles**:
- Mirror production code structure
- Separate test types (unit, integration, functional)
- Use conftest.py hierarchically for fixtures
- Follow naming conventions for discovery
- Use markers for selective test execution
- Keep test data separate from test logic

**Directory Layout**:
```
tests/
├── conftest.py           # Root fixtures
├── unit/                 # Fast, isolated tests
├── integration/          # Tests with dependencies
├── functional/           # End-to-end tests
└── fixtures/             # Test data
```

**Configuration Files**:
- `pytest.ini`: Pytest configuration
- `pyproject.toml`: Modern Python configuration
- `.coveragerc`: Coverage settings
