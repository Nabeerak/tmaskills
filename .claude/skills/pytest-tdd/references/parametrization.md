# Parametrization in Pytest

## Table of Contents

- [Introduction](#introduction)
- [Basic Parametrization](#basic-parametrization)
- [Multiple Parameters](#multiple-parameters)
- [Parametrize Combinations](#parametrize-combinations)
- [Custom Test IDs](#custom-test-ids)
- [Indirect Parametrization](#indirect-parametrization)
- [Parametrizing Fixtures](#parametrizing-fixtures)
- [Testing Edge Cases](#testing-edge-cases)
- [Table-Driven Tests](#table-driven-tests)
- [Advanced Patterns](#advanced-patterns)
- [Parametrization with Marks](#parametrization-with-marks)
- [Real-World Examples](#real-world-examples)
- [Best Practices](#best-practices)

---

## Introduction

**Parametrization** allows you to run the same test with different inputs, reducing code duplication and improving test coverage.

### Why Parametrize?

- **DRY Principle**: Write test logic once, test many scenarios
- **Comprehensive Testing**: Easily test edge cases and boundaries
- **Readability**: Clear separation of test data and test logic
- **Maintainability**: Change test logic in one place

### Basic Concept

```python
# Without parametrization - repetitive
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

def test_add_mixed_numbers():
    assert add(-2, 3) == 1

# With parametrization - concise
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-2, -3, -5),
    (-2, 3, 1)
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

---

## Basic Parametrization

### Single Parameter

```python
import pytest

@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_is_positive(number):
    assert number > 0
```

Output:
```
test_math.py::test_is_positive[1] PASSED
test_math.py::test_is_positive[2] PASSED
test_math.py::test_is_positive[3] PASSED
test_math.py::test_is_positive[4] PASSED
test_math.py::test_is_positive[5] PASSED
```

### Multiple Values

```python
@pytest.mark.parametrize("email", [
    "user@example.com",
    "test@test.co.uk",
    "admin@company.org"
])
def test_valid_email_format(email):
    assert "@" in email
    assert "." in email
```

### Tuple Parameters

```python
@pytest.mark.parametrize("width,height,expected_area", [
    (2, 3, 6),
    (5, 4, 20),
    (10, 10, 100)
])
def test_rectangle_area(width, height, expected_area):
    rectangle = Rectangle(width, height)
    assert rectangle.area() == expected_area
```

---

## Multiple Parameters

### Two Parameters

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("PyTest", "PYTEST")
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### Complex Data Structures

```python
@pytest.mark.parametrize("user_data,expected_valid", [
    ({"name": "Alice", "age": 25}, True),
    ({"name": "Bob", "age": -5}, False),
    ({"name": "", "age": 30}, False),
    ({"name": "Charlie", "age": 150}, False)
])
def test_user_validation(user_data, expected_valid):
    result = validate_user(user_data)
    assert result.is_valid == expected_valid
```

### Lists and Dictionaries

```python
@pytest.mark.parametrize("items,total", [
    ([1, 2, 3], 6),
    ([10, 20, 30], 60),
    ([], 0),
    ([100], 100)
])
def test_sum_items(items, total):
    assert sum(items) == total
```

---

## Parametrize Combinations

### Stacking Parametrize Decorators

```python
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [3, 4])
def test_add_combinations(x, y):
    """Generates 4 tests: (1,3), (1,4), (2,3), (2,4)"""
    result = add(x, y)
    assert result == x + y
```

Output:
```
test_math.py::test_add_combinations[3-1] PASSED
test_math.py::test_add_combinations[3-2] PASSED
test_math.py::test_add_combinations[4-1] PASSED
test_math.py::test_add_combinations[4-2] PASSED
```

### Cartesian Product

```python
@pytest.mark.parametrize("database", ["sqlite", "postgresql"])
@pytest.mark.parametrize("cache", [True, False])
@pytest.mark.parametrize("compression", ["gzip", "none"])
def test_configuration(database, cache, compression):
    """8 tests total: 2 databases × 2 cache options × 2 compression"""
    config = Config(
        database=database,
        cache_enabled=cache,
        compression=compression
    )
    assert config.is_valid()
```

### Selective Combinations

```python
@pytest.mark.parametrize("db,cache,expected", [
    ("sqlite", True, "fast"),
    ("sqlite", False, "slow"),
    ("postgresql", True, "fast"),
    ("postgresql", False, "medium")
])
def test_performance_category(db, cache, expected):
    result = get_performance_category(database=db, cache=cache)
    assert result == expected
```

---

## Custom Test IDs

### Using ids Parameter

```python
@pytest.mark.parametrize(
    "input,expected",
    [
        (2, 4),
        (3, 9),
        (4, 16)
    ],
    ids=["two_squared", "three_squared", "four_squared"]
)
def test_square(input, expected):
    assert input ** 2 == expected
```

Output:
```
test_math.py::test_square[two_squared] PASSED
test_math.py::test_square[three_squared] PASSED
test_math.py::test_square[four_squared] PASSED
```

### ID Function

```python
def id_from_user(user_data):
    """Generate test ID from user data."""
    return f"user_{user_data['name']}"

@pytest.mark.parametrize(
    "user_data",
    [
        {"name": "alice", "age": 25},
        {"name": "bob", "age": 30},
        {"name": "charlie", "age": 35}
    ],
    ids=id_from_user
)
def test_user_creation(user_data):
    user = User(**user_data)
    assert user.name == user_data["name"]
```

Output:
```
test_user.py::test_user_creation[user_alice] PASSED
test_user.py::test_user_creation[user_bob] PASSED
test_user.py::test_user_creation[user_charlie] PASSED
```

### Descriptive IDs

```python
@pytest.mark.parametrize(
    "url,status_code",
    [
        ("/", 200),
        ("/about", 200),
        ("/nonexistent", 404),
        ("/admin", 403)
    ],
    ids=[
        "home_page",
        "about_page",
        "not_found",
        "forbidden"
    ]
)
def test_endpoint_status(client, url, status_code):
    response = client.get(url)
    assert response.status_code == status_code
```

---

## Indirect Parametrization

Use `indirect` to pass parameters through fixtures.

### Basic Indirect

```python
@pytest.fixture
def user(request):
    """Create user from parameter."""
    user_type = request.param
    if user_type == "admin":
        return User(name="Admin", role="admin")
    elif user_type == "regular":
        return User(name="User", role="user")
    else:
        return User(name="Guest", role="guest")

@pytest.mark.parametrize("user", ["admin", "regular", "guest"], indirect=True)
def test_user_access(user):
    assert user.can_access_site()
```

### Partial Indirect

```python
@pytest.fixture
def database(request):
    """Create database from parameter."""
    db_type = request.param
    db = create_database(db_type)
    yield db
    db.close()

@pytest.mark.parametrize(
    "database,table_name",
    [
        ("sqlite", "users"),
        ("postgresql", "users"),
        ("sqlite", "products")
    ],
    indirect=["database"]  # Only database goes through fixture
)
def test_table_creation(database, table_name):
    database.create_table(table_name)
    assert database.has_table(table_name)
```

### Complex Indirect Setup

```python
@pytest.fixture
def api_client(request):
    """Create API client with specific version."""
    version = request.param
    client = APIClient(version=version)
    client.authenticate()
    yield client
    client.close()

@pytest.mark.parametrize(
    "api_client,endpoint",
    [
        ("v1", "/users"),
        ("v2", "/users"),
        ("v1", "/products"),
        ("v2", "/products")
    ],
    indirect=["api_client"]
)
def test_api_endpoint(api_client, endpoint):
    response = api_client.get(endpoint)
    assert response.status_code == 200
```

---

## Parametrizing Fixtures

### Fixture Parametrization

```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """Test with multiple database backends."""
    db_type = request.param
    db = create_database(db_type)
    db.initialize()
    yield db
    db.close()

def test_user_storage(database):
    """Runs 3 times, once per database."""
    user = User(name="Alice")
    database.save(user)

    retrieved = database.get_user(user.id)
    assert retrieved.name == "Alice"
```

### Parametrized Fixture with IDs

```python
@pytest.fixture(
    params=[
        {"host": "localhost", "port": 5432},
        {"host": "testdb", "port": 5432},
        {"host": "proddb", "port": 5433}
    ],
    ids=["local", "test_env", "prod_env"]
)
def db_config(request):
    return request.param

def test_database_connection(db_config):
    conn = connect(**db_config)
    assert conn.is_connected()
```

### Combining Fixture and Test Parametrization

```python
@pytest.fixture(params=[True, False])
def cache_enabled(request):
    """Test with cache on and off."""
    return request.param

@pytest.mark.parametrize("query_type", ["simple", "complex"])
def test_query_performance(cache_enabled, query_type):
    """4 tests: 2 cache states × 2 query types."""
    result = execute_query(query_type, cache=cache_enabled)
    assert result is not None
```

---

## Testing Edge Cases

### Boundary Testing

```python
@pytest.mark.parametrize("age,expected_category", [
    (0, "infant"),
    (1, "toddler"),
    (12, "child"),
    (13, "teen"),
    (17, "teen"),
    (18, "adult"),
    (64, "adult"),
    (65, "senior"),
    (100, "senior")
])
def test_age_category(age, expected_category):
    assert get_age_category(age) == expected_category
```

### Empty, Single, Many

```python
@pytest.mark.parametrize("items,expected_count", [
    ([], 0),           # Empty
    ([1], 1),          # Single
    ([1, 2], 2),       # Few
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10)  # Many
])
def test_item_count(items, expected_count):
    assert count_items(items) == expected_count
```

### Null and Special Values

```python
@pytest.mark.parametrize("value,is_valid", [
    (None, False),
    ("", False),
    ("   ", False),
    ("valid", True),
    ("a" * 1000, False),  # Too long
])
def test_string_validation(value, is_valid):
    result = validate_string(value)
    assert result == is_valid
```

### Error Cases

```python
@pytest.mark.parametrize("dividend,divisor,error", [
    (10, 0, ZeroDivisionError),
    ("10", 2, TypeError),
    (10, "2", TypeError),
    (None, 5, TypeError)
])
def test_division_errors(dividend, divisor, error):
    with pytest.raises(error):
        divide(dividend, divisor)
```

---

## Table-Driven Tests

### Data Table Pattern

```python
# Test data defined as a table
TEST_CASES = [
    # input_a, input_b, operation, expected
    (2, 3, "add", 5),
    (5, 3, "subtract", 2),
    (4, 3, "multiply", 12),
    (10, 2, "divide", 5),
    (10, 3, "divide", 3.33),
]

@pytest.mark.parametrize("a,b,op,expected", TEST_CASES)
def test_calculator(a, b, op, expected):
    calc = Calculator()
    result = calc.execute(a, b, op)
    assert abs(result - expected) < 0.01
```

### External Data

```python
# Load test cases from JSON
def load_test_cases():
    with open("test_data.json") as f:
        return json.load(f)

@pytest.mark.parametrize("test_case", load_test_cases())
def test_from_json(test_case):
    input_data = test_case["input"]
    expected = test_case["expected"]

    result = process(input_data)
    assert result == expected
```

### CSV Test Data

```python
import csv

def load_csv_tests():
    with open("test_data.csv") as f:
        reader = csv.DictReader(f)
        return [
            (row["username"], row["password"], row["should_succeed"] == "True")
            for row in reader
        ]

@pytest.mark.parametrize("username,password,should_succeed", load_csv_tests())
def test_authentication(username, password, should_succeed):
    result = authenticate(username, password)
    assert result.success == should_succeed
```

---

## Advanced Patterns

### Nested Parametrization

```python
USER_TYPES = ["admin", "user", "guest"]
ACTIONS = ["read", "write", "delete"]

PERMISSIONS = [
    ("admin", "read", True),
    ("admin", "write", True),
    ("admin", "delete", True),
    ("user", "read", True),
    ("user", "write", True),
    ("user", "delete", False),
    ("guest", "read", True),
    ("guest", "write", False),
    ("guest", "delete", False)
]

@pytest.mark.parametrize("user_type,action,allowed", PERMISSIONS)
def test_permissions(user_type, action, allowed):
    user = User(role=user_type)
    result = user.can_perform(action)
    assert result == allowed
```

### Parametrize Class

```python
@pytest.mark.parametrize("operation,a,b,expected", [
    ("add", 2, 3, 5),
    ("subtract", 5, 3, 2),
    ("multiply", 4, 3, 12)
])
class TestCalculator:
    def test_operation(self, operation, a, b, expected):
        calc = Calculator()
        result = getattr(calc, operation)(a, b)
        assert result == expected

    def test_operation_commutative(self, operation, a, b, expected):
        # Check if operation is commutative
        if operation in ["add", "multiply"]:
            calc = Calculator()
            result = getattr(calc, operation)(b, a)
            assert result == expected
```

### Dynamic Parametrization

```python
def generate_test_cases():
    """Generate test cases dynamically."""
    cases = []
    for i in range(1, 11):
        for j in range(1, 11):
            cases.append((i, j, i * j))
    return cases

@pytest.mark.parametrize("a,b,expected", generate_test_cases())
def test_multiplication(a, b, expected):
    assert a * b == expected
```

### Conditional Parametrization

```python
import sys

# Different test cases for different Python versions
if sys.version_info >= (3, 10):
    TEST_CASES = [
        ("match x: case 1: pass", True),
        ("def f(x): return x | y", True)
    ]
else:
    TEST_CASES = [
        ("lambda x: x", True),
        ("def f(x): return x or y", True)
    ]

@pytest.mark.parametrize("code,is_valid", TEST_CASES)
def test_syntax(code, is_valid):
    try:
        compile(code, "<string>", "exec")
        assert is_valid
    except SyntaxError:
        assert not is_valid
```

---

## Parametrization with Marks

### Skip Certain Parameters

```python
@pytest.mark.parametrize("value", [
    1,
    2,
    pytest.param(3, marks=pytest.mark.skip(reason="Known issue #123")),
    4
])
def test_value(value):
    assert process(value) > 0
```

### XFail for Known Issues

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    pytest.param("wörld", "WÖRLD", marks=pytest.mark.xfail(reason="Unicode bug")),
    ("test", "TEST")
])
def test_uppercase(input, expected):
    assert input.upper() == expected
```

### Conditional Marks

```python
import sys

@pytest.mark.parametrize("platform,command", [
    pytest.param(
        "windows",
        "dir",
        marks=pytest.mark.skipif(sys.platform != "win32", reason="Windows only")
    ),
    pytest.param(
        "linux",
        "ls",
        marks=pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
    )
])
def test_platform_command(platform, command):
    result = execute_command(command)
    assert result.returncode == 0
```

### Slow Tests

```python
@pytest.mark.parametrize("size", [
    10,
    100,
    pytest.param(10000, marks=pytest.mark.slow),
    pytest.param(100000, marks=pytest.mark.slow)
])
def test_processing_performance(size):
    data = generate_data(size)
    result = process(data)
    assert result is not None
```

---

## Real-World Examples

### Email Validation

```python
@pytest.mark.parametrize("email,is_valid", [
    # Valid emails
    ("user@example.com", True),
    ("test.user@example.com", True),
    ("user+tag@example.co.uk", True),
    ("123@example.com", True),

    # Invalid emails
    ("", False),
    ("notanemail", False),
    ("@example.com", False),
    ("user@", False),
    ("user @example.com", False),
    ("user@example", False),
])
def test_email_validation(email, is_valid):
    result = validate_email(email)
    assert result == is_valid
```

### URL Parsing

```python
@pytest.mark.parametrize("url,expected", [
    ("https://example.com", {"scheme": "https", "host": "example.com", "path": ""}),
    ("http://example.com/path", {"scheme": "http", "host": "example.com", "path": "/path"}),
    ("https://api.example.com:8080/v1/users", {
        "scheme": "https",
        "host": "api.example.com",
        "port": 8080,
        "path": "/v1/users"
    })
])
def test_url_parsing(url, expected):
    result = parse_url(url)
    for key, value in expected.items():
        assert getattr(result, key) == value
```

### Password Strength

```python
@pytest.mark.parametrize("password,expected_strength", [
    ("abc", "weak"),
    ("password", "weak"),
    ("Password1", "medium"),
    ("P@ssw0rd!", "strong"),
    ("MyS3cur3P@ssw0rd!", "strong"),
    ("", "weak"),
    ("a" * 100, "weak")
])
def test_password_strength(password, expected_strength):
    result = check_password_strength(password)
    assert result == expected_strength
```

### API Response Codes

```python
@pytest.mark.parametrize("endpoint,method,status", [
    ("/users", "GET", 200),
    ("/users", "POST", 201),
    ("/users/123", "GET", 200),
    ("/users/123", "PUT", 200),
    ("/users/123", "DELETE", 204),
    ("/users/999999", "GET", 404),
    ("/admin", "GET", 403)
])
def test_api_endpoints(client, endpoint, method, status):
    response = client.request(method, endpoint)
    assert response.status_code == status
```

### Date Calculations

```python
@pytest.mark.parametrize("start,days,expected", [
    ("2024-01-01", 1, "2024-01-02"),
    ("2024-01-31", 1, "2024-02-01"),
    ("2024-02-28", 1, "2024-02-29"),  # Leap year
    ("2024-12-31", 1, "2025-01-01"),
    ("2024-01-15", -5, "2024-01-10")
])
def test_add_days(start, days, expected):
    from datetime import datetime

    start_date = datetime.strptime(start, "%Y-%m-%d")
    result = add_days(start_date, days)
    expected_date = datetime.strptime(expected, "%Y-%m-%d")

    assert result == expected_date
```

### JSON Schema Validation

```python
VALID_USER_SCHEMAS = [
    {"name": "Alice", "email": "alice@example.com"},
    {"name": "Bob", "email": "bob@example.com", "age": 30}
]

INVALID_USER_SCHEMAS = [
    {},  # Missing required fields
    {"name": "Alice"},  # Missing email
    {"email": "alice@example.com"},  # Missing name
    {"name": "", "email": "alice@example.com"},  # Empty name
    {"name": "Alice", "email": "invalid"}  # Invalid email
]

@pytest.mark.parametrize("schema", VALID_USER_SCHEMAS)
def test_valid_user_schema(schema):
    assert validate_user_schema(schema).is_valid

@pytest.mark.parametrize("schema", INVALID_USER_SCHEMAS)
def test_invalid_user_schema(schema):
    assert not validate_user_schema(schema).is_valid
```

---

## Best Practices

### 1. Use Descriptive Parameter Names

```python
# ✓ Good
@pytest.mark.parametrize("user_age,expected_category", [
    (5, "child"),
    (15, "teen"),
    (25, "adult")
])

# ❌ Bad
@pytest.mark.parametrize("x,y", [
    (5, "child"),
    (15, "teen"),
    (25, "adult")
])
```

### 2. Add Custom IDs for Clarity

```python
# ✓ Good
@pytest.mark.parametrize(
    "value",
    [
        pytest.param(0, id="zero"),
        pytest.param(-1, id="negative"),
        pytest.param(1, id="positive")
    ]
)
def test_sign(value):
    ...
```

### 3. Keep Test Data Separate

```python
# ✓ Good
USER_TEST_CASES = [
    ("alice@example.com", True),
    ("invalid", False)
]

@pytest.mark.parametrize("email,is_valid", USER_TEST_CASES)
def test_email(email, is_valid):
    ...
```

### 4. Test Edge Cases

```python
@pytest.mark.parametrize("items", [
    [],              # Empty
    [1],             # Single
    [1, 2, 3],       # Multiple
    [1] * 1000       # Large
])
def test_process_items(items):
    result = process(items)
    assert result is not None
```

### 5. Use Marks for Special Cases

```python
@pytest.mark.parametrize("size", [
    10,
    100,
    pytest.param(10000, marks=pytest.mark.slow)
])
def test_performance(size):
    ...
```

### 6. Don't Over-Parametrize

```python
# ❌ Too many parameters - hard to read
@pytest.mark.parametrize("a,b,c,d,e,f,g", [...])

# ✓ Better - use objects
@pytest.mark.parametrize("config", [
    Config(a=1, b=2, c=3, ...),
    Config(a=4, b=5, c=6, ...)
])
```

---

## Summary

**Parametrization Benefits**:
- Reduce code duplication
- Test multiple scenarios easily
- Improve test coverage
- Clear test data separation

**Key Techniques**:
- **Basic**: `@pytest.mark.parametrize`
- **Fixtures**: `@pytest.fixture(params=...)`
- **Indirect**: Pass through fixtures
- **Stacking**: Combine parameters
- **Custom IDs**: Descriptive test names

**Best Practices**:
- Use descriptive names
- Add custom test IDs
- Test edge cases
- Keep data separate
- Don't over-parametrize
- Use marks for special cases

**Common Patterns**:
- Boundary testing
- Table-driven tests
- Error case testing
- External test data
