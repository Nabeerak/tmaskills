# Testing Best Practices

## Table of Contents

- [Introduction](#introduction)
- [Test Structure](#test-structure)
- [Test Independence](#test-independence)
- [Test Naming](#test-naming)
- [Test Data Management](#test-data-management)
- [Assertions](#assertions)
- [Test Organization](#test-organization)
- [Performance](#performance)
- [Maintainability](#maintainability)
- [Production-Ready Testing](#production-ready-testing)
- [Code Quality](#code-quality)
- [Documentation](#documentation)
- [CI/CD Integration](#cicd-integration)

---

## Introduction

**Best practices** ensure your tests are reliable, maintainable, and provide value to your development process.

### Characteristics of Good Tests

- **Fast**: Run quickly to enable frequent testing
- **Independent**: Don't depend on other tests
- **Repeatable**: Same result every time
- **Self-validating**: Clear pass/fail
- **Timely**: Written with or before code (TDD)

### FIRST Principles

- **F**ast
- **I**ndependent
- **R**epeatable
- **S**elf-validating
- **T**imely

---

## Test Structure

### Follow AAA Pattern

```python
# ✓ Good - Clear AAA structure
def test_user_registration():
    # Arrange
    user_data = {"email": "alice@example.com", "password": "SecurePass123"}

    # Act
    user = User.register(user_data)

    # Assert
    assert user.email == "alice@example.com"
    assert user.is_active is False
```

### One Assertion Concept Per Test

```python
# ✓ Good - Test one concept
def test_user_email_is_lowercase():
    user = User(email="ALICE@EXAMPLE.COM")
    assert user.email == "alice@example.com"

def test_user_email_is_validated():
    with pytest.raises(ValueError):
        User(email="invalid")

# ❌ Bad - Testing multiple concepts
def test_user_email():
    user = User(email="ALICE@EXAMPLE.COM")
    assert user.email == "alice@example.com"  # Lowercase
    assert "@" in user.email  # Validation

    with pytest.raises(ValueError):
        User(email="invalid")  # Different concept
```

### Keep Tests Simple

```python
# ✓ Good - Simple and readable
def test_calculate_total():
    cart = ShoppingCart()
    cart.add_item(Product(price=10))
    cart.add_item(Product(price=20))

    assert cart.total == 30

# ❌ Bad - Complex logic in test
def test_calculate_total_complex():
    cart = ShoppingCart()
    expected_total = 0

    for price in [10, 20, 30]:
        cart.add_item(Product(price=price))
        expected_total += price

    assert cart.total == expected_total
```

### Use Fixtures for Setup

```python
# ✓ Good - Fixture for reusable setup
@pytest.fixture
def shopping_cart():
    cart = ShoppingCart()
    cart.add_item(Product(name="Book", price=15))
    return cart

def test_cart_total(shopping_cart):
    assert shopping_cart.total == 15

def test_cart_item_count(shopping_cart):
    assert len(shopping_cart.items) == 1

# ❌ Bad - Repeated setup
def test_cart_total():
    cart = ShoppingCart()
    cart.add_item(Product(name="Book", price=15))
    assert cart.total == 15

def test_cart_item_count():
    cart = ShoppingCart()
    cart.add_item(Product(name="Book", price=15))
    assert len(cart.items) == 1
```

---

## Test Independence

### No Shared State

```python
# ❌ Bad - Shared mutable state
shared_users = []

def test_add_user():
    user = User(name="Alice")
    shared_users.append(user)
    assert len(shared_users) == 1

def test_another_user():
    # Fails if test_add_user runs first!
    assert len(shared_users) == 0

# ✓ Good - Independent tests
def test_add_user():
    users = []
    user = User(name="Alice")
    users.append(user)
    assert len(users) == 1

def test_another_user():
    users = []
    assert len(users) == 0
```

### Reset State Between Tests

```python
# ✓ Good - Fixture ensures clean state
@pytest.fixture
def database():
    db = Database(":memory:")
    db.initialize()
    yield db
    db.close()

def test_insert_user(database):
    database.insert(User(name="Alice"))
    assert database.count() == 1

def test_insert_product(database):
    # Gets fresh database
    database.insert(Product(name="Laptop"))
    assert database.count() == 1
```

### Avoid Test Order Dependencies

```python
# ❌ Bad - Depends on test order
def test_1_create_user():
    global user_id
    user = create_user("Alice")
    user_id = user.id

def test_2_update_user():
    # Depends on test_1_create_user
    update_user(user_id, name="Bob")

# ✓ Good - Independent tests
@pytest.fixture
def user():
    user = create_user("Alice")
    yield user
    delete_user(user.id)

def test_update_user(user):
    update_user(user.id, name="Bob")
    updated = get_user(user.id)
    assert updated.name == "Bob"
```

---

## Test Naming

### Descriptive Names

```python
# ✓ Good - Clear what's being tested
def test_user_registration_with_valid_email_creates_user():
    ...

def test_user_registration_with_duplicate_email_raises_error():
    ...

def test_password_hash_is_not_stored_in_plain_text():
    ...

# ❌ Bad - Vague names
def test_user():
    ...

def test_error():
    ...

def test_password():
    ...
```

### Pattern: test_unit_condition_expected

```python
def test_calculator_divide_by_zero_raises_error():
    # Unit: calculator
    # Condition: divide by zero
    # Expected: raises error
    with pytest.raises(ZeroDivisionError):
        Calculator().divide(10, 0)

def test_shopping_cart_with_discount_code_reduces_total():
    # Unit: shopping cart
    # Condition: with discount code
    # Expected: reduces total
    cart = ShoppingCart()
    cart.add_item(Product(price=100))
    cart.apply_discount("SAVE10")
    assert cart.total == 90
```

### Use Docstrings

```python
def test_user_login_with_valid_credentials():
    """
    Test that a user can successfully login with valid credentials.

    Given a registered user with email and password
    When the user attempts to login with correct credentials
    Then the authentication succeeds and returns user session
    """
    user = User.register(email="alice@example.com", password="SecurePass123")
    session = authenticate(email="alice@example.com", password="SecurePass123")

    assert session.user == user
    assert session.is_active is True
```

---

## Test Data Management

### Use Factories

```python
# ✓ Good - Factory for test data
@pytest.fixture
def user_factory():
    def create_user(**kwargs):
        defaults = {
            "name": "Test User",
            "email": "test@example.com",
            "role": "user"
        }
        return User(**{**defaults, **kwargs})
    return create_user

def test_admin_permissions(user_factory):
    admin = user_factory(role="admin")
    assert admin.can_delete_users() is True

def test_regular_user_permissions(user_factory):
    user = user_factory(role="user")
    assert user.can_delete_users() is False
```

### Separate Test Data

```python
# tests/fixtures/users.py
def get_valid_user_data():
    return {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25
    }

def get_invalid_user_data():
    return {
        "name": "",
        "email": "invalid",
        "age": -5
    }

# tests/test_users.py
from tests.fixtures.users import get_valid_user_data

def test_create_user_with_valid_data():
    user = User(**get_valid_user_data())
    assert user.name == "Alice"
```

### Use Parametrization for Multiple Cases

```python
# ✓ Good - Parametrize for multiple test cases
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("test@test.co.uk", True),
    ("invalid", False),
    ("@example.com", False),
    ("user@", False),
])
def test_email_validation(email, is_valid):
    result = validate_email(email)
    assert result == is_valid
```

### Avoid Magic Numbers

```python
# ❌ Bad - Magic numbers
def test_discount():
    total = calculate_discount(100, 10)
    assert total == 90

# ✓ Good - Named constants
def test_discount():
    original_price = 100
    discount_percentage = 10
    expected_price = 90

    total = calculate_discount(original_price, discount_percentage)
    assert total == expected_price
```

---

## Assertions

### Use Specific Assertions

```python
# ✓ Good - Specific assertions
assert user.is_active is True
assert user.email == "alice@example.com"
assert len(cart.items) == 3

# ❌ Bad - Generic assertions
assert user.is_active
assert user.email
assert cart.items
```

### Multiple Assertions for Same Concept

```python
# ✓ Good - Multiple assertions for complete verification
def test_user_registration():
    user = User.register(email="alice@example.com", password="pass123")

    # All verify the registration succeeded correctly
    assert user.email == "alice@example.com"
    assert user.password != "pass123"  # Hashed
    assert user.created_at is not None
    assert user.is_active is False  # Needs email verification
```

### Use pytest Helpers

```python
# ✓ Good - Use pytest.approx for floats
import pytest

def test_calculate_average():
    result = calculate_average([1.1, 2.2, 3.3])
    assert result == pytest.approx(2.2, abs=0.01)

# Use pytest.raises for exceptions
def test_invalid_input():
    with pytest.raises(ValueError, match="Invalid input"):
        process_data("invalid")
```

### Custom Error Messages

```python
# ✓ Good - Helpful error messages
def test_order_total():
    order = Order()
    order.add_item(Product(price=10))

    expected = 10
    actual = order.total

    assert actual == expected, \
        f"Order total mismatch: expected {expected}, got {actual}"
```

---

## Test Organization

### Mirror Production Structure

```
src/myapp/
├── models/
│   ├── user.py
│   └── product.py
└── services/
    ├── user_service.py
    └── order_service.py

tests/
├── unit/
│   ├── models/
│   │   ├── test_user.py
│   │   └── test_product.py
│   └── services/
│       ├── test_user_service.py
│       └── test_order_service.py
└── integration/
    └── test_api.py
```

### Group Related Tests

```python
# ✓ Good - Grouped in class
class TestUserAuthentication:
    def test_login_with_valid_credentials_succeeds(self):
        ...

    def test_login_with_invalid_password_fails(self):
        ...

    def test_login_with_nonexistent_user_fails(self):
        ...

class TestUserRegistration:
    def test_registration_with_valid_data_creates_user(self):
        ...

    def test_registration_with_duplicate_email_fails(self):
        ...
```

### Use Markers

```python
# ✓ Good - Use markers for organization
@pytest.mark.slow
def test_large_dataset_processing():
    ...

@pytest.mark.integration
def test_database_connection():
    ...

@pytest.mark.smoke
def test_critical_functionality():
    ...

# Run specific markers
# pytest -m "not slow"
# pytest -m "smoke"
```

---

## Performance

### Keep Tests Fast

```python
# ✓ Good - Mock slow operations
@patch('myapp.send_email')
def test_user_registration(mock_send_email):
    User.register(email="alice@example.com")
    mock_send_email.assert_called_once()

# ❌ Bad - Actually send email
def test_user_registration():
    User.register(email="alice@example.com")
    # Waits for real email to send (slow!)
```

### Use In-Memory Databases

```python
# ✓ Good - In-memory database for speed
@pytest.fixture
def database():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

# ❌ Bad - Real database (slower)
@pytest.fixture
def database():
    engine = create_engine("postgresql://localhost/test_db")
    return engine
```

### Parallel Test Execution

```bash
# Run tests in parallel
pip install pytest-xdist
pytest -n auto
```

### Scope Fixtures Appropriately

```python
# ✓ Good - Session-scoped for expensive setup
@pytest.fixture(scope="session")
def app():
    """Create app once for all tests."""
    return create_app(testing=True)

# ✓ Good - Function-scoped for isolation
@pytest.fixture
def user():
    """Create fresh user for each test."""
    return User(name="Test User")
```

---

## Maintainability

### Don't Test Implementation Details

```python
# ❌ Bad - Testing private methods
def test_internal_calculation():
    calculator = Calculator()
    result = calculator._internal_helper(5)
    assert result == 10

# ✓ Good - Test public interface
def test_calculate():
    calculator = Calculator()
    result = calculator.calculate(5)
    assert result == expected_output
```

### Avoid Brittle Tests

```python
# ❌ Bad - Brittle, depends on exact HTML
def test_render_user_page():
    html = render_user_page(user)
    assert html == '<div class="user"><h1>Alice</h1></div>'

# ✓ Good - Test meaningful content
def test_render_user_page():
    html = render_user_page(user)
    assert user.name in html
    assert "user" in html
```

### Use Test Doubles Appropriately

```python
# ✓ Good - Mock external dependencies
@patch('requests.get')
def test_fetch_user_data(mock_get):
    mock_get.return_value.json.return_value = {"name": "Alice"}
    user = fetch_user_data(123)
    assert user["name"] == "Alice"

# ❌ Bad - Mocking your own code
@patch('myapp.calculate_total')  # Your own function!
def test_checkout(mock_calculate):
    mock_calculate.return_value = 100
    total = checkout()
    assert total == 100
```

### Keep Tests DRY

```python
# ✓ Good - Reusable helper
def create_test_order(items):
    order = Order()
    for item in items:
        order.add_item(item)
    return order

def test_order_total():
    order = create_test_order([Product(price=10), Product(price=20)])
    assert order.total == 30

def test_order_count():
    order = create_test_order([Product(price=10), Product(price=20)])
    assert len(order.items) == 2
```

---

## Production-Ready Testing

### Test Error Handling

```python
def test_handles_network_error():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.ConnectionError("Network error")

        with pytest.raises(ServiceUnavailable):
            fetch_data()

def test_handles_invalid_json():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")

        with pytest.raises(DataError):
            fetch_data()
```

### Test Edge Cases

```python
@pytest.mark.parametrize("value,expected", [
    (0, "zero"),           # Zero
    (-1, "negative"),      # Negative
    (1, "positive"),       # Positive
    (sys.maxsize, "max"),  # Maximum
    (None, "none"),        # Null
    ("", "empty"),         # Empty string
])
def test_edge_cases(value, expected):
    result = process(value)
    assert result == expected
```

### Test Security

```python
def test_password_is_hashed():
    user = User(email="alice@example.com", password="plain_password")
    user.save()

    # Password should not be stored in plain text
    assert user.password != "plain_password"
    assert len(user.password) > 50  # Hashed passwords are longer

def test_sql_injection_prevented():
    # Attempt SQL injection
    malicious_input = "'; DROP TABLE users; --"

    with pytest.raises(ValidationError):
        User.search(malicious_input)
```

### Test Performance Requirements

```python
import time

def test_response_time_under_threshold():
    start = time.time()
    result = process_large_dataset()
    duration = time.time() - start

    assert duration < 1.0, f"Processing took {duration}s, expected < 1s"
```

### Test Backwards Compatibility

```python
def test_legacy_api_format_still_supported():
    # Old format
    result = api_call({"userId": 123})  # Deprecated but still supported
    assert result.success is True

    # New format
    result = api_call({"user_id": 123})
    assert result.success is True
```

---

## Code Quality

### Use Type Hints in Tests

```python
# ✓ Good - Type hints improve clarity
from typing import List

def test_filter_active_users() -> None:
    users: List[User] = [
        User(name="Alice", active=True),
        User(name="Bob", active=False)
    ]

    active: List[User] = filter_active_users(users)

    assert len(active) == 1
    assert active[0].name == "Alice"
```

### Lint Your Tests

```bash
# Run linters on test code too
flake8 tests/
pylint tests/
mypy tests/
```

### Code Review Test Code

```python
# ✓ Good - Review tests like production code
# - Check for clarity
# - Verify assertions
# - Look for duplication
# - Ensure proper isolation
```

---

## Documentation

### Document Complex Tests

```python
def test_complex_workflow():
    """
    Test the complete user registration and activation workflow.

    Steps:
    1. User submits registration form
    2. System creates inactive user account
    3. System sends activation email
    4. User clicks activation link
    5. System activates user account

    Verifies:
    - User account is created correctly
    - Activation email is sent
    - User can activate their account
    - Activated user can login
    """
    # Test implementation
```

### Use Given-When-Then

```python
def test_user_can_reset_password():
    """
    Given a registered user who forgot their password
    When they request a password reset
    Then they receive a reset email with a valid token
    """
    # Given
    user = User.register(email="alice@example.com", password="old_pass")

    # When
    reset_token = request_password_reset(user.email)

    # Then
    assert reset_token is not None
    assert validate_reset_token(reset_token) is True
```

---

## CI/CD Integration

### Run Tests in CI

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run tests
      run: |
        pytest --cov=myapp --cov-fail-under=80

    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

### Different Test Stages

```yaml
# Fast tests on every commit
test-unit:
  script: pytest tests/unit -v

# Integration tests on merge to main
test-integration:
  script: pytest tests/integration -v
  only:
    - main

# Full test suite nightly
test-full:
  script: pytest tests/ -v --slow
  schedule:
    - cron: "0 0 * * *"
```

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

---

## Summary

**Key Principles**:
- **FIRST**: Fast, Independent, Repeatable, Self-validating, Timely
- **AAA**: Arrange, Act, Assert
- **DRY**: Don't Repeat Yourself
- **SOLID**: Apply to test code too

**Best Practices**:
- Write tests first (TDD)
- One assertion concept per test
- Use descriptive names
- Keep tests independent
- Mock external dependencies
- Test edge cases and errors
- Maintain high coverage
- Review and refactor tests

**Production Ready**:
- Test error handling
- Test security
- Test performance
- Test backwards compatibility
- Document complex tests
- Integrate with CI/CD

**Maintainability**:
- Don't test implementation
- Avoid brittle tests
- Use fixtures wisely
- Keep tests DRY
- Type hints and linting
- Code review test code

**Remember**: Tests are code too. Apply the same quality standards to tests as you do to production code.
