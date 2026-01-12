# Code Coverage with Pytest

## Table of Contents

- [Introduction](#introduction)
- [Installing Coverage](#installing-coverage)
- [Basic Coverage Usage](#basic-coverage-usage)
- [Coverage Configuration](#coverage-configuration)
- [Coverage Reports](#coverage-reports)
- [Branch Coverage](#branch-coverage)
- [Coverage Thresholds](#coverage-thresholds)
- [Excluding Code from Coverage](#excluding-code-from-coverage)
- [Coverage with CI/CD](#coverage-with-cicd)
- [Coverage Best Practices](#coverage-best-practices)
- [Understanding Coverage Metrics](#understanding-coverage-metrics)
- [Common Pitfalls](#common-pitfalls)
- [Advanced Patterns](#advanced-patterns)

---

## Introduction

**Code coverage** measures which lines of code are executed during testing, helping identify untested code paths.

### Why Measure Coverage?

- **Find Gaps**: Identify untested code
- **Quality Metric**: Track testing completeness
- **Confidence**: Higher coverage generally means better testing
- **Refactoring**: Safe to refactor covered code
- **Documentation**: Shows which features are tested

### Coverage Metrics

- **Line Coverage**: Percentage of lines executed
- **Branch Coverage**: Percentage of branches (if/else) taken
- **Function Coverage**: Percentage of functions called
- **Statement Coverage**: Percentage of statements executed

### Coverage is Not Everything

```python
# 100% coverage doesn't mean bug-free!
def divide(a, b):
    return a / b  # Covered, but what about b=0?

def test_divide():
    assert divide(10, 2) == 5  # 100% coverage, but incomplete
```

---

## Installing Coverage

### Installation

```bash
# Install pytest-cov (includes coverage.py)
pip install pytest-cov

# Or just coverage.py
pip install coverage
```

### Verify Installation

```bash
pytest --cov --help
```

---

## Basic Coverage Usage

### Run Tests with Coverage

```bash
# Basic coverage
pytest --cov

# Coverage for specific module
pytest --cov=myapp

# Coverage for multiple modules
pytest --cov=myapp --cov=mylib

# Coverage with specific test directory
pytest tests/ --cov=myapp
```

### Example Output

```
---------- coverage: platform linux, python 3.11 -----------
Name                 Stmts   Miss  Cover
----------------------------------------
myapp/__init__.py        2      0   100%
myapp/models.py         45      3    93%
myapp/services.py       67     12    82%
myapp/utils.py          23      0   100%
----------------------------------------
TOTAL                  137     15    89%
```

### Terminal Report

```bash
# Show missing lines
pytest --cov=myapp --cov-report=term-missing

# Output:
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
myapp/models.py         45      3    93%   23, 45-47
myapp/services.py       67     12    82%   34, 56-67
```

---

## Coverage Configuration

### pytest.ini Configuration

```ini
[pytest]
addopts =
    --cov=myapp
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
addopts = [
    "--cov=myapp",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80"
]

[tool.coverage.run]
source = ["myapp"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__pycache__/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "class .*\\bProtocol\\):",
    "@(abc\\.)?abstractmethod"
]
```

### .coveragerc Configuration

```ini
[run]
source = myapp
omit =
    */tests/*
    */migrations/*
    */__pycache__/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod

precision = 2
show_missing = True

[html]
directory = htmlcov
```

---

## Coverage Reports

### Terminal Report

```bash
# Simple terminal report
pytest --cov=myapp --cov-report=term

# Terminal report with missing lines
pytest --cov=myapp --cov-report=term-missing

# Detailed terminal report
pytest --cov=myapp --cov-report=term:skip-covered
```

### HTML Report

```bash
# Generate HTML report
pytest --cov=myapp --cov-report=html

# Open in browser
open htmlcov/index.html
```

HTML report shows:
- Color-coded coverage (green = covered, red = not covered)
- Line-by-line view
- Branch coverage visualization
- Interactive navigation

### XML Report (for CI/CD)

```bash
# Generate XML report (for tools like Codecov, Coveralls)
pytest --cov=myapp --cov-report=xml

# Creates coverage.xml file
```

### JSON Report

```bash
# Generate JSON report
pytest --cov=myapp --cov-report=json

# Creates coverage.json file
```

### Multiple Reports

```bash
# Generate multiple report types
pytest --cov=myapp \
    --cov-report=html \
    --cov-report=xml \
    --cov-report=term-missing
```

### Annotated Source

```bash
# Generate annotated source files
pytest --cov=myapp --cov-report=annotate

# Creates .py,cover files showing coverage
```

---

## Branch Coverage

### Enable Branch Coverage

```bash
# Test branch coverage
pytest --cov=myapp --cov-branch
```

### Example

```python
# myapp/validator.py
def validate_age(age):
    if age < 0:        # Branch 1
        return False
    elif age > 150:    # Branch 2
        return False
    else:              # Branch 3
        return True

# tests/test_validator.py
def test_negative_age():
    assert validate_age(-5) is False  # Covers branch 1

def test_valid_age():
    assert validate_age(25) is True   # Covers branch 3

# Missing: branch 2 (age > 150)
```

Coverage report with `--cov-branch`:
```
Name                   Stmts   Miss Branch BrPart  Cover
----------------------------------------------------------
myapp/validator.py         5      0      4      1    88%
```

### Configuration

```ini
[tool.coverage.run]
branch = true
```

---

## Coverage Thresholds

### Minimum Coverage

```bash
# Fail if coverage below 80%
pytest --cov=myapp --cov-fail-under=80
```

### Configuration

```ini
# pytest.ini
[pytest]
addopts = --cov-fail-under=80

# .coveragerc
[report]
fail_under = 80
```

### CI/CD Integration

```bash
# Exit with error code if below threshold
pytest --cov=myapp --cov-fail-under=80 || exit 1
```

### Per-Module Thresholds

```python
# Use coverage contexts for different thresholds
# Not directly supported, but can check in scripts

import json

with open('coverage.json') as f:
    data = json.load(f)

for file, stats in data['files'].items():
    coverage = stats['summary']['percent_covered']

    if 'critical' in file and coverage < 95:
        print(f"Critical file {file} below 95%: {coverage}%")
        exit(1)
    elif coverage < 80:
        print(f"File {file} below 80%: {coverage}%")
        exit(1)
```

---

## Excluding Code from Coverage

### Pragma Comments

```python
def debug_function():  # pragma: no cover
    """Debug function not tested in production."""
    import pdb
    pdb.set_trace()

def main():
    if __name__ == "__main__":  # pragma: no cover
        run_app()
```

### Exclude Specific Lines

```python
def complex_function(value):
    try:
        result = process(value)
    except Exception as e:  # pragma: no cover
        # Error handling not covered in tests
        logger.error(f"Error: {e}")
        raise

    return result
```

### Exclude Patterns

```ini
# .coveragerc
[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
    @overload
```

### Exclude Files

```ini
[run]
omit =
    */tests/*
    */migrations/*
    */venv/*
    */__pycache__/*
    */conftest.py
    setup.py
```

### Exclude Directories

```ini
[run]
source = myapp
omit =
    myapp/legacy/*
    myapp/experimental/*
    myapp/migrations/*
```

---

## Coverage with CI/CD

### GitHub Actions

```yaml
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
        pip install pytest pytest-cov

    - name: Run tests with coverage
      run: |
        pytest --cov=myapp --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v2
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### GitLab CI

```yaml
test:
  image: python:3.11
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - pytest --cov=myapp --cov-report=xml --cov-report=term
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

### Jenkins

```groovy
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pip install pytest pytest-cov'
                sh 'pytest --cov=myapp --cov-report=xml --cov-report=html'
            }
        }
    }

    post {
        always {
            publishHTML([
                reportDir: 'htmlcov',
                reportFiles: 'index.html',
                reportName: 'Coverage Report'
            ])
        }
    }
}
```

### Codecov Integration

```bash
# Install codecov
pip install codecov

# Upload coverage
codecov
```

With `.codecov.yml`:

```yaml
coverage:
  status:
    project:
      default:
        target: 80%
        threshold: 1%
    patch:
      default:
        target: 80%

ignore:
  - "tests/"
  - "setup.py"
  - "migrations/"
```

---

## Coverage Best Practices

### 1. Aim for High Coverage, Not 100%

```python
# Focus on testing business logic
def calculate_discount(price, percentage):
    """Critical business logic - should have 100% coverage."""
    if percentage < 0 or percentage > 100:
        raise ValueError("Invalid percentage")
    return price * (1 - percentage / 100)

# Less critical code can have lower coverage
def format_currency(amount):  # pragma: no cover
    """Display formatting - less critical."""
    return f"${amount:.2f}"
```

### 2. Test Edge Cases

```python
@pytest.mark.parametrize("age,expected", [
    (0, "infant"),      # Boundary
    (1, "toddler"),     # Just above boundary
    (12, "child"),      # Normal
    (13, "teen"),       # Boundary
    (17, "teen"),       # Just below boundary
    (18, "adult"),      # Boundary
    (65, "senior"),     # Boundary
    (150, "senior")     # Maximum
])
def test_age_categories(age, expected):
    assert get_category(age) == expected
```

### 3. Don't Test Just for Coverage

```python
# ❌ Bad - Testing implementation details
def test_internal_method():
    obj = MyClass()
    obj._internal_helper()  # Private method

# ✓ Good - Test public behavior
def test_public_behavior():
    obj = MyClass()
    result = obj.public_method()
    assert result == expected
```

### 4. Use Coverage to Find Gaps

```python
# Coverage shows this branch is never tested
def process_order(order):
    if order.total > 1000:
        apply_discount(order)  # Missing test!
    return order
```

Add missing test:

```python
def test_large_order_discount():
    order = Order(total=1500)
    result = process_order(order)
    assert result.discount_applied is True
```

### 5. Monitor Coverage Trends

```bash
# Track coverage over time
pytest --cov=myapp --cov-report=json

# Compare with previous coverage
python scripts/check_coverage_trend.py
```

### 6. Different Thresholds for Different Code

```python
# Critical code: 95%+ coverage
# myapp/payment/processor.py

# Business logic: 80%+ coverage
# myapp/services/*.py

# UI/Display code: 60%+ coverage
# myapp/formatters/*.py

# Scripts/Tools: Lower priority
# scripts/*.py - pragma: no cover acceptable
```

---

## Understanding Coverage Metrics

### Line Coverage

```python
def example(x):
    if x > 0:           # Line 2 - Covered
        return "pos"    # Line 3 - Covered
    else:
        return "neg"    # Line 5 - Not covered

# Test only positive case
def test_positive():
    assert example(5) == "pos"

# Line coverage: 80% (4/5 lines)
```

### Branch Coverage

```python
def grade(score):
    if score >= 90:         # Branch: True, False
        return "A"
    elif score >= 80:       # Branch: True, False
        return "B"
    else:
        return "F"

# Only test one path
def test_a_grade():
    assert grade(95) == "A"

# Line coverage: High
# Branch coverage: Low (only 1/4 branches)
```

### Function Coverage

```python
class Calculator:
    def add(self, a, b):        # Covered
        return a + b

    def multiply(self, a, b):   # Not covered
        return a * b

    def divide(self, a, b):     # Not covered
        return a / b

def test_add():
    calc = Calculator()
    assert calc.add(2, 3) == 5

# Function coverage: 33% (1/3 methods)
```

### Statement Coverage

```python
def process(data):
    result = []                    # Statement 1 - Covered
    for item in data:              # Statement 2 - Covered
        if item > 0:               # Statement 3 - Covered
            result.append(item)    # Statement 4 - Covered
    return result                  # Statement 5 - Covered

def test_process():
    assert process([1, 2, 3]) == [1, 2, 3]

# Statement coverage: 100%
```

---

## Common Pitfalls

### 1. Chasing 100% Coverage

```python
# ❌ Don't test trivial code just for coverage
def test_repr():
    user = User(name="Alice")
    repr(user)  # Just calling for coverage

# ✓ Focus on meaningful tests
def test_user_creation():
    user = User(name="Alice")
    assert user.name == "Alice"
```

### 2. Ignoring Branch Coverage

```python
# Line coverage: 100%, but missing branches
def validate(value):
    if value:
        return True
    return False

def test_validate():
    assert validate("data") is True
    # Missing: test_validate with falsy value
```

### 3. Coverage Without Assertions

```python
# ❌ Bad - Coverage without verification
def test_process():
    process_data()  # Executes but doesn't verify anything

# ✓ Good - Coverage with assertions
def test_process():
    result = process_data()
    assert result.success is True
```

### 4. Excluding Too Much

```python
# ❌ Bad - Excluding important code
def critical_calculation():  # pragma: no cover
    # This should be tested!
    return complex_math()

# ✓ Good - Only exclude truly untestable code
def debug_helper():  # pragma: no cover
    import pdb; pdb.set_trace()
```

### 5. Not Reviewing Coverage Reports

```bash
# Generate and review HTML report regularly
pytest --cov=myapp --cov-report=html
open htmlcov/index.html

# Look for:
# - Red lines (not covered)
# - Patterns in missing coverage
# - Critical paths without tests
```

---

## Advanced Patterns

### Coverage Contexts

```python
# Track which tests cover which code
# pytest.ini
[pytest]
addopts = --cov=myapp --cov-context=test

# .coveragerc
[run]
dynamic_context = test_function
```

### Parallel Coverage

```bash
# Run tests in parallel with coverage
pytest -n auto --cov=myapp --cov-report=html

# Requires pytest-xdist and coverage with parallel support
```

### Coverage Diff

```python
# coverage_diff.py
import json

def compare_coverage(old_file, new_file):
    with open(old_file) as f:
        old = json.load(f)

    with open(new_file) as f:
        new = json.load(f)

    old_pct = old['totals']['percent_covered']
    new_pct = new['totals']['percent_covered']

    diff = new_pct - old_pct

    if diff < 0:
        print(f"Coverage decreased by {abs(diff):.2f}%")
        exit(1)
    else:
        print(f"Coverage improved by {diff:.2f}%")
```

### Source Code Coverage

```bash
# Only measure coverage for source code, not tests
pytest tests/ --cov=myapp --cov-report=term-missing
```

### Coverage for Specific Tests

```bash
# Coverage for specific test file
pytest tests/test_users.py --cov=myapp.users

# Coverage for specific test function
pytest tests/test_users.py::test_create_user --cov=myapp.users
```

---

## Summary

**Coverage Basics**:
- Install: `pip install pytest-cov`
- Run: `pytest --cov=myapp`
- Reports: term, html, xml, json

**Configuration**:
- pytest.ini or pyproject.toml
- Set thresholds with `--cov-fail-under`
- Exclude code with pragma comments

**Best Practices**:
- Aim for 80%+ coverage
- Focus on business logic
- Use branch coverage
- Review coverage reports
- Don't chase 100%

**Key Metrics**:
- Line coverage
- Branch coverage
- Function coverage
- Statement coverage

**Tools**:
- pytest-cov: Coverage plugin
- Codecov/Coveralls: Cloud coverage tracking
- HTML reports: Visual coverage inspection
- CI/CD: Automated coverage checks

**Remember**: Coverage is a tool, not a goal. High coverage doesn't guarantee quality, but low coverage often indicates gaps in testing.
