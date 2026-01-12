# Security in Testing

## Table of Contents

- [Secrets Management](#secrets-management)
- [Sensitive Test Data](#sensitive-test-data)
- [Secure Mocking Practices](#secure-mocking-practices)
- [Environment Variables](#environment-variables)
- [Best Practices](#best-practices)
- [Common Vulnerabilities](#common-vulnerabilities)

---

## Secrets Management

### Never Hardcode Secrets

```python
# ❌ BAD - Hardcoded credentials
def test_api_authentication():
    api_key = "sk-1234567890abcdef"  # NEVER DO THIS!
    response = authenticate(api_key)
    assert response.status_code == 200

# ✓ GOOD - Use environment variables
import os

def test_api_authentication():
    api_key = os.getenv("TEST_API_KEY")
    response = authenticate(api_key)
    assert response.status_code == 200
```

### Use Pytest Fixtures for Secrets

```python
# conftest.py
import os
import pytest

@pytest.fixture
def api_credentials():
    """Provide API credentials from environment."""
    return {
        "api_key": os.getenv("TEST_API_KEY"),
        "api_secret": os.getenv("TEST_API_SECRET")
    }

# test_api.py
def test_api_call(api_credentials):
    response = call_api(api_credentials["api_key"])
    assert response.status_code == 200
```

### pytest-env Plugin

```ini
# pytest.ini
[pytest]
env =
    TEST_API_KEY=dummy-key-for-testing
    TEST_DATABASE_URL=sqlite:///:memory:
```

```bash
# Install
pip install pytest-env
```

---

## Sensitive Test Data

### Use Fake Data Libraries

```python
from faker import Faker

@pytest.fixture
def fake_user_data():
    """Generate fake user data for testing."""
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "ssn": fake.ssn(),  # Fake SSN, not real PII
        "address": fake.address()
    }

def test_user_creation(fake_user_data):
    user = create_user(fake_user_data)
    assert user.email == fake_user_data["email"]
```

### Anonymize Production Data

```python
# ❌ BAD - Using real production data
def test_user_processing():
    user = {
        "name": "John Smith",  # Real person
        "email": "john.smith@realcompany.com",  # Real email
        "ssn": "123-45-6789"  # Real SSN - NEVER!
    }
    process_user(user)

# ✓ GOOD - Anonymized test data
def test_user_processing():
    user = {
        "name": "Test User",
        "email": "test@example.com",
        "ssn": "000-00-0000"  # Clearly fake
    }
    process_user(user)
```

### Factory Pattern for Test Data

```python
# test_factories.py
import factory
from faker import Faker

fake = Faker()

class UserFactory(factory.Factory):
    class Meta:
        model = dict

    name = factory.LazyFunction(fake.name)
    email = factory.LazyFunction(fake.email)
    phone = factory.LazyFunction(fake.phone_number)

# Usage in tests
def test_user_creation():
    user_data = UserFactory()
    user = create_user(user_data)
    assert user.email == user_data["email"]
```

---

## Secure Mocking Practices

### Don't Log Sensitive Data in Mocks

```python
# ❌ BAD - Mock might log sensitive data
def test_password_hashing(mocker):
    mock_hash = mocker.patch("myapp.auth.hash_password")
    mock_hash.return_value = "hashed"

    result = hash_password("super_secret_password")

    # This assertion logs the password!
    mock_hash.assert_called_with("super_secret_password")

# ✓ GOOD - Verify without logging sensitive data
def test_password_hashing(mocker):
    mock_hash = mocker.patch("myapp.auth.hash_password")
    mock_hash.return_value = "hashed"

    result = hash_password("super_secret_password")

    # Just verify it was called, don't log args
    assert mock_hash.call_count == 1
    assert result == "hashed"
```

### Custom Marker for Sensitive Tests

```python
# conftest.py
import pytest

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "sensitive: mark test as handling sensitive data"
    )

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Sanitize output for sensitive tests
    if "sensitive" in item.keywords:
        if report.longrepr:
            # Redact sensitive information from test output
            report.longrepr = "[REDACTED - Sensitive test output]"

# test_auth.py
@pytest.mark.sensitive
def test_password_reset():
    token = generate_reset_token("user@example.com")
    assert len(token) == 64
```

---

## Environment Variables

### .env.test Files

```bash
# .env.test (add to .gitignore!)
TEST_API_KEY=test-key-not-real
TEST_DATABASE_URL=sqlite:///:memory:
TEST_AWS_ACCESS_KEY=fake-access-key
TEST_AWS_SECRET_KEY=fake-secret-key
```

```python
# conftest.py
import pytest
from dotenv import load_dotenv
import os

@pytest.fixture(scope="session", autouse=True)
def load_test_env():
    """Load test environment variables."""
    load_dotenv(".env.test")
    yield
    # Cleanup if needed
```

### Environment-Specific Fixtures

```python
# conftest.py
import pytest
import os

@pytest.fixture
def test_database_url():
    """Provide test database URL from environment."""
    url = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
    return url

@pytest.fixture
def production_like_db_url():
    """Use PostgreSQL for integration tests."""
    if os.getenv("CI"):
        return os.getenv("CI_DATABASE_URL")
    return "postgresql://test:test@localhost:5432/test_db"
```

---

## Best Practices

### 1. Separate Test Credentials from Production

```python
# config.py
import os

class Config:
    API_KEY = os.getenv("API_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")

class TestConfig(Config):
    API_KEY = os.getenv("TEST_API_KEY", "dummy-test-key")
    DATABASE_URL = "sqlite:///:memory:"
    TESTING = True

# conftest.py
@pytest.fixture(scope="session")
def app_config():
    return TestConfig()
```

### 2. Use Secret Scanners

```bash
# Install git-secrets
brew install git-secrets  # macOS
apt-get install git-secrets  # Linux

# Setup
git secrets --install
git secrets --register-aws

# Scan repository
git secrets --scan
```

### 3. Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

### 4. Review Test Output

```python
# conftest.py
import pytest

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Redact common secrets from output
    if report.longrepr:
        output = str(report.longrepr)
        # Redact patterns that look like API keys
        import re
        output = re.sub(r'sk-[a-zA-Z0-9]{32,}', '[REDACTED-API-KEY]', output)
        output = re.sub(r'Bearer [a-zA-Z0-9-._~+/]+=*', 'Bearer [REDACTED]', output)
        report.longrepr = output
```

---

## Common Vulnerabilities

### 1. Hardcoded Database Passwords

```python
# ❌ BAD
DATABASE_URL = "postgresql://admin:P@ssw0rd123@localhost/testdb"

# ✓ GOOD
DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")
```

### 2. API Keys in Version Control

```python
# ❌ BAD - Committed to git
API_KEY = "sk-1234567890abcdef"

# ✓ GOOD - Use environment
API_KEY = os.getenv("TEST_API_KEY")

# Add to .gitignore
# .env.test
# .env.local
# secrets/
```

### 3. Logging Sensitive Information

```python
# ❌ BAD - Logs password
def test_authentication():
    password = "user_password"
    print(f"Testing with password: {password}")  # NEVER!
    result = authenticate("user", password)

# ✓ GOOD - No sensitive data in logs
def test_authentication():
    result = authenticate("test_user", "test_password")
    assert result.is_authenticated
```

### 4. Shared Test Credentials

```python
# ❌ BAD - Shared across team, committed
TEST_API_KEY = "shared-team-key-123"  # Everyone uses same key

# ✓ GOOD - Individual test credentials
# Each developer has their own .env.test (not committed)
TEST_API_KEY = os.getenv("TEST_API_KEY")  # Personal test key
```

### 5. Production Data in Tests

```python
# ❌ BAD - Using production database
@pytest.fixture
def database_url():
    return "postgresql://admin:pass@prod.db.company.com/prod"

# ✓ GOOD - Isolated test database
@pytest.fixture
def database_url():
    return "sqlite:///:memory:"  # In-memory for tests
```

---

## Security Checklist

Before committing tests:

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] All credentials loaded from environment variables
- [ ] .env.test file added to .gitignore
- [ ] No real PII or sensitive data in test fixtures
- [ ] Test output doesn't log sensitive information
- [ ] Mocks don't expose credentials in assertions
- [ ] Separate test credentials from production
- [ ] Secret scanner configured (git-secrets, detect-secrets)
- [ ] Pre-commit hooks check for secrets
- [ ] Test database isolated from production
