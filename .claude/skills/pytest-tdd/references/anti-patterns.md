# Testing Anti-Patterns

## Table of Contents

- [Test Structure Anti-Patterns](#test-structure-anti-patterns)
- [Test Independence Anti-Patterns](#test-independence-anti-patterns)
- [Assertion Anti-Patterns](#assertion-anti-patterns)
- [Mocking Anti-Patterns](#mocking-anti-patterns)
- [Fixture Anti-Patterns](#fixture-anti-patterns)
- [Coverage Anti-Patterns](#coverage-anti-patterns)
- [TDD Anti-Patterns](#tdd-anti-patterns)
- [Performance Anti-Patterns](#performance-anti-patterns)

---

## Test Structure Anti-Patterns

### 1. Testing Multiple Behaviors

**Problem**: One test verifying multiple unrelated behaviors.

```python
# ❌ Bad - Tests multiple behaviors
def test_user():
    user = User("Alice", "alice@example.com")

    # Testing name update
    user.update_name("Bob")
    assert user.name == "Bob"

    # Testing email update
    user.update_email("bob@example.com")
    assert user.email == "bob@example.com"

    # Testing deactivation
    user.deactivate()
    assert user.is_active is False
```

**Solution**: One test per behavior.

```python
# ✓ Good - Separate tests
def test_update_name_changes_user_name():
    user = User("Alice", "alice@example.com")
    user.update_name("Bob")
    assert user.name == "Bob"

def test_update_email_changes_user_email():
    user = User("Alice", "alice@example.com")
    user.update_email("bob@example.com")
    assert user.email == "bob@example.com"

def test_deactivate_sets_is_active_to_false():
    user = User("Alice", "alice@example.com")
    user.deactivate()
    assert user.is_active is False
```

### 2. Vague Test Names

**Problem**: Test names that don't describe what's being tested.

```python
# ❌ Bad - Unclear names
def test_user():
    ...

def test_calculation():
    ...

def test_edge_case():
    ...
```

**Solution**: Descriptive names explaining behavior.

```python
# ✓ Good - Clear names
def test_user_registration_with_valid_data_creates_user():
    ...

def test_divide_by_zero_raises_zero_division_error():
    ...

def test_empty_cart_checkout_raises_validation_error():
    ...
```

### 3. Missing AAA Structure

**Problem**: Unstructured tests mixing setup, action, and verification.

```python
# ❌ Bad - No clear structure
def test_login():
    user = User("test@example.com", "password")
    assert login(user.email, user.password) is True
```

**Solution**: Clear AAA (Arrange-Act-Assert) structure.

```python
# ✓ Good - Clear phases
def test_login_with_valid_credentials_succeeds():
    # Arrange
    user = User("test@example.com", "password")

    # Act
    result = login(user.email, user.password)

    # Assert
    assert result is True
```

---

## Test Independence Anti-Patterns

### 4. Tests Depending on Execution Order

**Problem**: Tests that only pass when run in specific order.

```python
# ❌ Bad - Tests depend on order
user_id = None

def test_create_user():
    global user_id
    user = create_user("Alice")
    user_id = user.id
    assert user_id is not None

def test_get_user():
    # Depends on test_create_user running first
    user = get_user(user_id)
    assert user.name == "Alice"
```

**Solution**: Independent tests with proper setup.

```python
# ✓ Good - Independent tests
@pytest.fixture
def test_user(db_session):
    user = create_user("Alice")
    return user

def test_create_user_returns_user_with_id():
    user = create_user("Alice")
    assert user.id is not None
    assert user.name == "Alice"

def test_get_user_returns_correct_user(test_user):
    user = get_user(test_user.id)
    assert user.name == "Alice"
```

### 5. Shared Mutable State

**Problem**: Tests modifying shared objects causing failures.

```python
# ❌ Bad - Shared state
SHARED_LIST = []

def test_add_item():
    SHARED_LIST.append(1)
    assert len(SHARED_LIST) == 1

def test_remove_item():
    # Fails if test_add_item ran first
    assert len(SHARED_LIST) == 0
```

**Solution**: Isolated state per test.

```python
# ✓ Good - Isolated state
@pytest.fixture
def my_list():
    return []

def test_add_item(my_list):
    my_list.append(1)
    assert len(my_list) == 1

def test_list_starts_empty(my_list):
    assert len(my_list) == 0
```

### 6. Persistent Test Data

**Problem**: Tests creating data that persists across runs.

```python
# ❌ Bad - Data persists
def test_create_user(db):
    user = User(email="test@example.com")
    db.add(user)
    db.commit()  # User remains in database
```

**Solution**: Clean up after tests.

```python
# ✓ Good - Automatic cleanup
@pytest.fixture
def db_session():
    session = create_session()
    yield session
    session.rollback()  # Rollback changes
    session.close()

def test_create_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    # Automatically rolled back after test
```

---

## Assertion Anti-Patterns

### 7. No Assertions

**Problem**: Tests that don't verify anything.

```python
# ❌ Bad - No assertion
def test_create_user():
    user = create_user("Alice")
    # Test passes even if create_user is broken
```

**Solution**: Always include assertions.

```python
# ✓ Good - Clear assertions
def test_create_user_returns_user_object():
    user = create_user("Alice")
    assert user is not None
    assert user.name == "Alice"
```

### 8. Assertion Roulette

**Problem**: Multiple assertions without clear messages.

```python
# ❌ Bad - Which assertion failed?
def test_user_data():
    user = get_user(1)
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.age == 30
    assert user.is_active is True
```

**Solution**: Clear assertion messages or separate tests.

```python
# ✓ Good - Clear messages
def test_user_data():
    user = get_user(1)
    assert user.name == "Alice", f"Expected name 'Alice', got '{user.name}'"
    assert user.email == "alice@example.com", "Email mismatch"
    assert user.age == 30, f"Expected age 30, got {user.age}"
    assert user.is_active is True, "User should be active"

# Or better - separate tests
def test_user_has_correct_name():
    user = get_user(1)
    assert user.name == "Alice"

def test_user_has_correct_email():
    user = get_user(1)
    assert user.email == "alice@example.com"
```

### 9. Testing with print()

**Problem**: Using print statements instead of assertions.

```python
# ❌ Bad - No verification
def test_calculation():
    result = calculate(2, 3)
    print(f"Result: {result}")  # Not a test!
```

**Solution**: Use assertions to verify.

```python
# ✓ Good - Actual verification
def test_calculation_returns_correct_result():
    result = calculate(2, 3)
    assert result == 5
```

---

## Mocking Anti-Patterns

### 10. Mocking Everything

**Problem**: Over-mocking makes tests fragile and meaningless.

```python
# ❌ Bad - Mocking too much
def test_user_service(mocker):
    mock_db = mocker.Mock()
    mock_validator = mocker.Mock()
    mock_hasher = mocker.Mock()
    mock_logger = mocker.Mock()

    service = UserService(mock_db, mock_validator, mock_hasher, mock_logger)
    # Test becomes meaningless - everything is mocked
```

**Solution**: Mock only external dependencies.

```python
# ✓ Good - Mock external dependencies only
def test_user_service_creates_user(mocker):
    # Mock only database (external dependency)
    mock_db = mocker.Mock()

    # Use real validator and hasher (internal logic)
    service = UserService(mock_db)

    user_data = {"name": "Alice", "email": "alice@example.com"}
    service.create_user(user_data)

    # Verify database interaction
    mock_db.add.assert_called_once()
```

### 11. Not Verifying Mock Calls

**Problem**: Mocking but not verifying the mock was used correctly.

```python
# ❌ Bad - No verification
def test_send_email(mocker):
    mock_smtp = mocker.patch("myapp.email.SMTP")
    send_email("user@example.com", "Hello")
    # Test passes even if SMTP was never called
```

**Solution**: Verify mock interactions.

```python
# ✓ Good - Verify calls
def test_send_email_calls_smtp(mocker):
    mock_smtp = mocker.patch("myapp.email.SMTP")

    send_email("user@example.com", "Hello")

    mock_smtp.assert_called_once()
    mock_smtp.return_value.send_message.assert_called_once()
```

### 12. Mocking What You Don't Own

**Problem**: Mocking third-party library internals.

```python
# ❌ Bad - Mocking requests internals
def test_api_call(mocker):
    mocker.patch("requests.adapters.HTTPAdapter.send")
    # Fragile - breaks if requests changes internals
```

**Solution**: Mock at your API boundary.

```python
# ✓ Good - Mock your wrapper
def test_api_call(mocker):
    mocker.patch("myapp.api_client.make_request")
    # Test your code, not requests library
```

---

## Fixture Anti-Patterns

### 13. Fixture Overuse

**Problem**: Creating fixtures for everything, even simple data.

```python
# ❌ Bad - Unnecessary fixture
@pytest.fixture
def number_two():
    return 2

@pytest.fixture
def number_three():
    return 3

def test_add(number_two, number_three):
    assert add(number_two, number_three) == 5
```

**Solution**: Use fixtures for complex setup only.

```python
# ✓ Good - Simple data inline
def test_add():
    assert add(2, 3) == 5

# Fixtures for complex setup
@pytest.fixture
def db_with_test_data(db_session):
    # Complex setup
    users = [User(name=f"User{i}") for i in range(10)]
    db_session.add_all(users)
    db_session.commit()
    return db_session
```

### 14. Fixtures with Side Effects

**Problem**: Fixtures that modify global state.

```python
# ❌ Bad - Modifies environment
@pytest.fixture
def set_env():
    os.environ["API_KEY"] = "test-key"
    # Never cleaned up - affects other tests
```

**Solution**: Clean up side effects with yield.

```python
# ✓ Good - Cleanup after test
@pytest.fixture
def set_env():
    original = os.environ.get("API_KEY")
    os.environ["API_KEY"] = "test-key"

    yield

    # Cleanup
    if original:
        os.environ["API_KEY"] = original
    else:
        del os.environ["API_KEY"]
```

---

## Coverage Anti-Patterns

### 15. Chasing 100% Coverage

**Problem**: Writing meaningless tests just to hit 100% coverage.

```python
# ❌ Bad - Testing getters/setters for coverage
def test_user_name_getter():
    user = User("Alice")
    assert user.name == "Alice"  # Pointless test

def test_user_name_setter():
    user = User("Alice")
    user.name = "Bob"
    assert user.name == "Bob"  # Not testing behavior
```

**Solution**: Focus on testing behavior, not code coverage.

```python
# ✓ Good - Test meaningful behavior
def test_user_name_update_triggers_audit_log():
    user = User("Alice")

    user.name = "Bob"

    assert user.audit_log.last_entry.action == "name_changed"
    assert user.audit_log.last_entry.old_value == "Alice"
```

### 16. Ignoring Low Coverage Areas

**Problem**: Using coverage exclusions to hide untested code.

```python
# ❌ Bad - Hiding untested code
def complex_business_logic():  # pragma: no cover
    # Critical code marked as "no cover" to boost coverage
    ...
```

**Solution**: Write tests for critical code or acknowledge tech debt.

```python
# ✓ Good - Test critical paths
def test_complex_business_logic_with_valid_input():
    result = complex_business_logic(valid_input)
    assert result.is_valid

# Acceptable - Skip truly untestable code
def __repr__(self):  # pragma: no cover
    return f"User({self.name})"
```

---

## TDD Anti-Patterns

### 17. Writing Tests After Code

**Problem**: Writing implementation first, then tests.

**Why it's bad**: Not following TDD, tests become verification of implementation rather than specification.

**Solution**: Follow Red-Green-Refactor cycle strictly.

### 18. Skipping Refactor Phase

**Problem**: Moving to next feature without refactoring.

```python
# ❌ Bad - No refactoring
def calculate_discount(price, percent):
    return price - (price * percent / 100)  # Works but could be better

# Immediately move to next feature
```

**Solution**: Refactor after green phase.

```python
# ✓ Good - Refactor for clarity
def calculate_discount(price: float, percent: float) -> float:
    """Calculate discounted price.

    Args:
        price: Original price
        percent: Discount percentage (0-100)

    Returns:
        Discounted price
    """
    if not 0 <= percent <= 100:
        raise ValueError("Percent must be between 0 and 100")

    return price * (1 - percent / 100)
```

### 19. Writing Too Much Code in Green Phase

**Problem**: Over-engineering during green phase.

```python
# ❌ Bad - Too much code for green phase
def add(a, b):
    # Adding features not required by test
    if not isinstance(a, (int, float)):
        raise TypeError("...")
    if not isinstance(b, (int, float)):
        raise TypeError("...")

    result = a + b
    logger.info(f"Added {a} + {b} = {result}")

    return result
```

**Solution**: Minimal code to pass test.

```python
# ✓ Good - Minimal for green
def add(a, b):
    return a + b

# Add validation in refactor phase when you write test for it
```

---

## Performance Anti-Patterns

### 20. Slow Tests with sleep()

**Problem**: Using time.sleep() in tests.

```python
# ❌ Bad - Slow tests
def test_async_task():
    trigger_async_task()
    time.sleep(5)  # Wait for task to complete
    assert task_completed()
```

**Solution**: Use proper async testing or mocking.

```python
# ✓ Good - Fast tests with mocking
def test_async_task(mocker):
    mock_task = mocker.patch("myapp.tasks.async_task")
    trigger_async_task()
    mock_task.assert_called_once()

# Or use async tests
@pytest.mark.asyncio
async def test_async_task():
    result = await async_task()
    assert result.completed
```

### 21. Not Using Test Parallelization

**Problem**: Running slow tests sequentially.

```bash
# ❌ Bad - Slow
pytest tests/  # Takes 10 minutes
```

**Solution**: Use pytest-xdist for parallel execution.

```bash
# ✓ Good - Fast
pytest tests/ -n auto  # Runs in parallel
```

---

## Summary

**Key Anti-Patterns to Avoid**:
- Testing multiple behaviors in one test
- Tests depending on execution order
- Over-mocking or not verifying mocks
- Chasing 100% coverage without meaningful tests
- Using sleep() instead of proper async testing
- Writing tests after implementation
- Vague test names

**Best Practices**:
- One test, one behavior
- Independent tests with isolated state
- Clear AAA structure
- Mock external dependencies only
- Focus on behavior, not coverage percentage
- Follow TDD Red-Green-Refactor cycle
- Descriptive test names
