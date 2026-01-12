---
name: pytest-tdd
description: |
  Implement Test-Driven Development workflows with pytest including unit and integration
  tests, fixtures, parametrization, mocking, AAA pattern, async testing, code coverage,
  and test organization. This skill should be used when users ask to write tests, set up
  pytest, implement TDD workflows, create fixtures, mock dependencies, or measure code
  coverage for Python applications.
---

# Pytest TDD

Implement production-ready Test-Driven Development workflows with pytest following industry best practices.

## What This Skill Does

- Sets up pytest with proper project structure and configuration
- Implements TDD workflow (Red-Green-Refactor cycle)
- Creates unit and integration tests with AAA pattern
- Designs fixtures for test setup and teardown
- Implements parametrized tests for multiple input scenarios
- Mocks external dependencies (APIs, databases, file systems)
- Configures code coverage measurement and reporting
- Tests async code and FastAPI applications
- Organizes tests with conftest.py and proper structure

## What This Skill Does NOT Do

- Write production code without tests (this is TDD-focused)
- Test frontend JavaScript/TypeScript (use dedicated JS testing tools)
- Performance or load testing (use locust, JMeter)
- Deploy test infrastructure to CI/CD (use separate DevOps patterns)
- Generate test data at scale (use factories like faker, factory_boy)

## Requirements

**Core Dependencies**:
- pytest 8.0+ (core testing framework)
- pytest-cov 7.0+ (coverage measurement)

**Optional Dependencies** (install as needed):
- pytest-asyncio 0.23+ (async testing) - `pip install pytest-asyncio`
- pytest-mock 3.12+ (enhanced mocking) - `pip install pytest-mock`
- pytest-env 1.1+ (environment variables) - `pip install pytest-env`
- pytest-xdist 3.5+ (parallel execution) - `pip install pytest-xdist`
- faker 20.0+ (fake test data) - `pip install faker`

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing test structure, testing patterns, production code to test |
| **Conversation** | Test requirements, coverage goals, testing scope (unit/integration) |
| **Skill References** | Pytest patterns from `references/` (fixtures, mocking, AAA pattern) |
| **User Guidelines** | Team testing standards, coverage thresholds, CI/CD constraints |

### Codebase Scanning Checklist

Before writing tests, scan for project-specific patterns:

**Test Structure**:
- Check `tests/` directory structure (unit/, integration/, conftest.py locations)
- Identify test file naming patterns (`test_*.py` vs `*_test.py`)
- Note fixture organization (global conftest.py vs module-level)

**Naming Conventions**:
- Review existing test function names (prefix patterns, descriptive style)
- Check fixture naming style (snake_case conventions, descriptive names)
- Identify pytest marker usage (`@pytest.mark.slow`, custom markers)

**Configuration**:
- Read `pytest.ini` or `pyproject.toml` for existing settings (test paths, coverage config)
- Check for plugins in use (pytest-asyncio, pytest-mock, pytest-cov)
- Note any custom pytest hooks in conftest.py files

**Import Patterns**:
- Observe how production code is imported in existing tests
- Check for shared test utilities or helper modules
- Identify common fixture patterns (database sessions, API clients)

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER'S specific context:

1. **Testing Scope**: "What needs to be tested?" (specific functions, modules, API endpoints)
2. **Test Type**: "Unit tests, integration tests, or both?" (determines fixture complexity)
3. **External Dependencies**: "What external services are used?" (APIs, databases, file systems - affects mocking strategy)
4. **Coverage Goals**: "What's the target code coverage?" (default: 80%, clarify if not mentioned)
5. **Existing Tests**: "Are there existing tests to extend?" (determines structure approach)

**Question Pacing**: Ask 1-2 questions at a time. Infer from context where possible to avoid over-asking.

**If User Doesn't Answer**: Use sensible defaults (unit tests, 80% coverage, standard pytest structure) and mention assumptions in implementation.

## Optional Clarifications

Ask if context suggests need:

- **Async Code**: "Testing async functions or FastAPI endpoints?" (requires pytest-asyncio)
- **Database Tests**: "Need database fixtures with rollback?" (affects fixture design)
- **Snapshot Testing**: "Need snapshot/regression testing?" (requires pytest-snapshot)
- **CI/CD Integration**: "Running tests in CI/CD?" (affects configuration and reporting format)
- **Parallel Execution**: "Need parallel test execution?" (requires pytest-xdist)

---

## TDD Workflow (Red-Green-Refactor)

Follow the three-phase TDD cycle:

1. **RED**: Write a failing test for functionality that doesn't exist yet
2. **GREEN**: Write minimal code to make the test pass
3. **REFACTOR**: Improve code quality without changing behavior

**Repeat** for each new feature.

See `references/tdd-workflow.md` for complete examples with Red-Green-Refactor iterations.

---

## Test Organization

Structure tests to mirror production code:

```
project/
├── src/myapp/
├── tests/
│   ├── conftest.py           # Shared fixtures
│   ├── unit/                 # Fast, isolated tests
│   ├── integration/          # Tests with dependencies
│   └── functional/           # End-to-end tests
├── pytest.ini
└── pyproject.toml
```

See `references/test-organization.md` for detailed structure patterns.

---

## AAA Pattern (Arrange-Act-Assert)

Structure every test with three phases:

```python
def test_user_registration():
    # Arrange: Set up test data
    user_data = {"email": "test@example.com", "password": "secret"}
    # Act: Execute the code being tested
    result = register_user(user_data)
    # Assert: Verify the outcome
    assert result.is_success
```

See `references/aaa-pattern.md` for comprehensive examples and anti-patterns.

---

## Fixtures

Create reusable test setup:

```python
@pytest.fixture
def database_session():
    """Provide database session with automatic rollback."""
    session = create_session()
    yield session
    session.rollback()
    session.close()
```

**Scopes**: `function` (default), `class`, `module`, `session`

See `references/fixtures.md` for comprehensive fixture patterns including parametrized fixtures and dependency injection.

---

## Parametrization

Test multiple inputs with one test:

```python
@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_addition(a, b, expected):
    assert add(a, b) == expected
```

See `references/parametrization.md` for parametrized fixtures and edge case testing.

---

## Edge Case Testing

Systematically test boundary conditions and edge cases:

**Common Edge Cases**: Empty inputs (None, "", []), boundary values (0, -1, max/min), invalid types, large inputs, special characters (Unicode, escape sequences).

```python
@pytest.mark.parametrize("invalid_input", [None, "", [], {}, -1, float('inf')])
def test_function_handles_invalid_input(invalid_input):
    with pytest.raises(ValueError):
        process_input(invalid_input)
```

See `references/parametrization.md` for comprehensive edge case patterns.

---

## Mocking

Mock external dependencies:

```python
def test_api_call(monkeypatch):
    """Test API call without hitting real endpoint."""
    def mock_get(*args, **kwargs):
        return {"status": "success", "data": [1, 2, 3]}

    monkeypatch.setattr("myapp.api.requests.get", mock_get)
    result = fetch_data()
    assert result["status"] == "success"
```

See `references/mocking.md` for mocking strategies (APIs, databases, file systems) and pytest-mock patterns.

---

## Async Testing

Test async code with pytest-asyncio:

```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None
```

See `references/async-testing.md` for FastAPI testing with TestClient/AsyncClient.

---

## Code Coverage

Measure test coverage:

```bash
# Run tests with coverage
pytest --cov=myapp --cov-report=html tests/

# Configuration in pytest.ini
[pytest]
addopts = --cov=myapp --cov-report=html --cov-report=term-missing
```

See `references/coverage.md` for detailed coverage configuration and reporting.

---

## Security in Tests

Protect sensitive data and credentials in test code:

**Secrets Management**:
- Never hardcode API keys, tokens, or passwords in test files
- Use environment variables: `os.getenv("API_KEY")` or pytest fixtures
- Use `.env.test` files (add to `.gitignore`)
- Consider `pytest-env` plugin for test-specific environment variables

**Sensitive Test Data**:
- Anonymize or use fake PII in tests (use `faker` library for realistic fake data)
- Don't use production data in test suites
- Sanitize test outputs to avoid logging credentials

**Secure Mocking**:
- Verify mocks don't accidentally log sensitive data in assertions
- Use `pytest.mark.sensitive` for tests with sensitive data (custom marker)
- Review test outputs before committing

See `references/security-testing.md` for comprehensive security patterns and secret scanning.

---

## Error Handling & Debugging

When tests fail or encounter issues:

**Debugging Failed Tests**:
- Use `-v` flag for verbose output: `pytest -v`
- Use `-s` flag to see print statements: `pytest -s`
- Use `--pdb` to drop into debugger on failure: `pytest --pdb`
- Use `--lf` to run only last failed tests: `pytest --lf`

**Interpreting Errors**:
- `AssertionError`: Expected vs actual values don't match (check assertion logic)
- `FixtureLookupError`: Fixture not found (check conftest.py and fixture names)
- `TypeError/AttributeError`: Mock not configured properly (verify mock setup)

**Recovery Strategies**:
- Isolate failing test: `pytest tests/test_file.py::test_function`
- Check fixture teardown: Ensure cleanup happens even on failure
- Review test dependencies: Tests should be independent

See `references/best-practices.md` for debugging strategies.

---

## FastAPI Testing

Test FastAPI endpoints:

```python
from fastapi.testclient import TestClient

def test_create_user(client):
    response = client.post("/users", json={"email": "test@example.com"})
    assert response.status_code == 201
    assert "id" in response.json()
```

See `references/async-testing.md` for comprehensive FastAPI testing patterns.

---

## Official Documentation

For latest patterns and updates, refer to:

| Resource | URL | Use For |
|----------|-----|---------|
| Pytest | https://docs.pytest.org/ | Core framework, fixtures, markers |
| pytest-cov | https://pytest-cov.readthedocs.io/ | Coverage measurement and reporting |
| pytest-asyncio | https://pytest-asyncio.readthedocs.io/ | Testing async code |
| pytest-mock | https://pytest-mock.readthedocs.io/ | Mocking with pytest |

**Version Compatibility**: Patterns current as of pytest 8.0+, pytest-cov 7.0+, pytest-asyncio 0.23+. Check official docs for latest features.

**For Unlisted Patterns**: If a pattern or plugin is not covered in this skill's references, fetch the latest official documentation using WebFetch. The pytest ecosystem is extensive—consult official docs for specialized plugins (pytest-xdist, pytest-benchmark, etc.) and advanced patterns.

---

## Standards to Follow

### Must Follow
- [ ] Use AAA pattern for all tests (Arrange, Act, Assert)
- [ ] Write descriptive test names that explain what is being tested
- [ ] Test one behavior per test function
- [ ] Use fixtures for shared test setup
- [ ] Mock external dependencies (APIs, databases, file systems)
- [ ] Organize tests to mirror production code structure
- [ ] Use parametrize for testing multiple inputs
- [ ] Aim for 80%+ code coverage on critical paths
- [ ] Use type hints in test functions
- [ ] Add docstrings to complex tests
- [ ] Keep unit tests fast (<100ms per test)
- [ ] Mark slow tests with @pytest.mark.slow
- [ ] Profile slow tests with --durations=10 flag

### Must Avoid
- [ ] Don't test implementation details (test behavior, not internals)
- [ ] Don't use sleep() for timing (use proper async or mocking)
- [ ] Don't share state between tests (use fixtures with proper scope)
- [ ] Don't hardcode test data in test functions (use fixtures or parametrize)
- [ ] Don't hardcode secrets/credentials in tests (use env vars or fixtures)
- [ ] Don't use production data in test suites (use fake/anonymized data)
- [ ] Don't skip tests without clear reason and ticket reference
- [ ] Don't mock what you don't own unless necessary
- [ ] Don't test external libraries (trust they work)
- [ ] Don't write tests that depend on test execution order
- [ ] Don't write non-deterministic tests (fix flaky tests immediately)
- [ ] Don't depend on external state (time.time(), random without seed)

See `references/best-practices.md` and `references/anti-patterns.md` for detailed guidance.

---

## Output Checklist

Before delivering, verify:

**Test Structure**
- [ ] Tests organized in unit/ and integration/ directories
- [ ] conftest.py files at appropriate levels with shared fixtures
- [ ] Tests mirror production code structure

**Test Quality**
- [ ] All tests follow AAA pattern (Arrange, Act, Assert)
- [ ] Descriptive test names that explain behavior
- [ ] One behavior tested per test function
- [ ] Type hints on test functions

**Fixtures and Mocking**
- [ ] Fixtures created for reusable setup
- [ ] Proper fixture scopes (function, class, module, session)
- [ ] External dependencies mocked appropriately
- [ ] Database tests use fixtures with rollback

**Coverage and Reporting**
- [ ] pytest.ini or pyproject.toml configured
- [ ] Code coverage meets target threshold (default 80%)
- [ ] Coverage report excludes test files and migrations
- [ ] HTML coverage report generated

**TDD Workflow**
- [ ] Tests written before production code (if applicable)
- [ ] Tests initially failed (Red phase documented)
- [ ] Minimal code written to pass tests (Green phase)
- [ ] Code refactored with tests still passing

**Documentation**
- [ ] README includes test running instructions
- [ ] Complex tests have docstrings explaining what they test
- [ ] Fixture purposes documented

**CI/CD Integration** (if applicable)
- [ ] Test markers configured for CI environments (@pytest.mark.slow, @pytest.mark.integration)
- [ ] JUnit XML report generated for CI: pytest --junitxml=test-results.xml
- [ ] Parallel execution configured if needed: pytest -n auto (requires pytest-xdist)
- [ ] Test output optimized for CI readability

**Standards Verification**
- [ ] All "Must Follow" items from Standards to Follow section verified
- [ ] All "Must Avoid" anti-patterns checked and confirmed absent
- [ ] Edge cases systematically tested (empty, boundary, invalid inputs)
- [ ] Security checks: No hardcoded secrets, no production data in tests
- [ ] Codebase scanning completed (naming conventions, fixture patterns matched)

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/tdd-workflow.md` | Complete TDD cycle with Red-Green-Refactor examples |
| `references/test-organization.md` | Project structure and conftest.py patterns |
| `references/aaa-pattern.md` | Arrange-Act-Assert examples and anti-patterns |
| `references/fixtures.md` | Fixture scopes, yield fixtures, parametrized fixtures |
| `references/parametrization.md` | Testing multiple inputs and edge cases |
| `references/mocking.md` | Mocking strategies for APIs, databases, file systems |
| `references/async-testing.md` | Testing async code and FastAPI applications |
| `references/coverage.md` | Coverage configuration and reporting |
| `references/security-testing.md` | Secrets management, secure mocking, PII handling |
| `references/best-practices.md` | Production-ready testing patterns |
| `references/anti-patterns.md` | Common testing mistakes to avoid |

**Finding Specific Topics**: All reference files include a table of contents. For quick searches across all references, use these grep patterns:

```bash
# Fixture patterns
grep -r "@pytest.fixture\|yield\|scope=" references/

# Mocking patterns
grep -r "monkeypatch\|mocker\|patch\|mock" references/

# Parametrization
grep -r "@pytest.mark.parametrize\|params=" references/

# Async testing
grep -r "@pytest.mark.asyncio\|async def test\|AsyncClient" references/

# Coverage configuration
grep -r "pytest-cov\|--cov\|coverage" references/

# AAA pattern
grep -r "# Arrange\|# Act\|# Assert" references/

# FastAPI testing
grep -r "TestClient\|AsyncClient\|app.include_router" references/

# Security patterns
grep -r "os.getenv\|pytest.mark.sensitive\|faker\|secrets" references/
```

---

## Assets

| File | Purpose |
|------|---------|
| `assets/templates/pytest.ini` | Pytest configuration template |
| `assets/templates/pyproject.toml` | Modern pytest configuration |
| `assets/templates/conftest.py` | Example conftest with common fixtures |
| `assets/templates/test_example.py` | Complete test file with AAA pattern |
| `assets/templates/test_async.py` | Async testing examples |
| `assets/templates/.coveragerc` | Coverage configuration template |
