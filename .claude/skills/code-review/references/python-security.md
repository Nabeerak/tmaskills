# Python Security Patterns

Security-specific patterns and vulnerabilities for Python code review.

---

## Table of Contents

1. [Injection Vulnerabilities](#injection-vulnerabilities)
2. [Insecure Deserialization](#insecure-deserialization)
3. [Command Injection](#command-injection)
4. [Path Traversal](#path-traversal)
5. [Cryptography](#cryptography)
6. [Web Framework Security](#web-framework-security)
7. [Dependencies](#dependencies)
8. [Configuration](#configuration)

---

## Injection Vulnerabilities

### SQL Injection

```python
# ❌ CRITICAL: SQL injection
username = request.args.get('username')
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
# Attack: username='; DROP TABLE users; --

# ❌ Also vulnerable
query = "SELECT * FROM users WHERE username = '%s'" % username
cursor.execute(query)

# ✅ Use parameterized queries
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))

# ✅ With SQLAlchemy ORM
from sqlalchemy import text
user = db.session.execute(
    text("SELECT * FROM users WHERE username = :username"),
    {"username": username}
).first()

# ✅ Best: Use ORM methods
user = User.query.filter_by(username=username).first()
```

### NoSQL Injection (MongoDB)

```python
# ❌ MongoDB injection
from pymongo import MongoClient
username = request.json.get('username')
password = request.json.get('password')

user = db.users.find_one({
    'username': username,
    'password': password
})
# Attack: {"username": {"$ne": null}, "password": {"$ne": null}}

# ✅ Validate input types
if not isinstance(username, str) or not isinstance(password, str):
    abort(400, 'Invalid input types')

user = db.users.find_one({
    'username': username,
    'password': password
})

# ✅ Use schema validation
from pydantic import BaseModel, validator

class LoginSchema(BaseModel):
    username: str
    password: str

    @validator('username', 'password')
    def validate_string(cls, v):
        if not isinstance(v, str):
            raise ValueError('Must be string')
        return v
```

### LDAP Injection

```python
# ❌ LDAP injection
import ldap
search_filter = f"(uid={username})"
# Attack: username=*)(uid=*))(|(uid=*

# ✅ Escape special characters
import ldap.filter
search_filter = ldap.filter.escape_filter_chars(username)
search_filter = f"(uid={search_filter})"
```

---

## Insecure Deserialization

### Pickle Deserialization

```python
# ❌ CRITICAL: Remote code execution
import pickle
data = pickle.loads(untrusted_input)  # Can execute arbitrary code

# Attack payload example:
# class Exploit:
#     def __reduce__(self):
#         import os
#         return (os.system, ('rm -rf /',))

# ✅ Use JSON instead
import json
data = json.loads(untrusted_input)

# ✅ If you MUST use pickle, use restricted unpickler
import pickle
import io

class RestrictedUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Only allow safe classes
        if module == "builtins" and name in ['list', 'dict', 'str', 'int']:
            return getattr(__builtins__, name)
        raise pickle.UnpicklingError(f"global '{module}.{name}' is forbidden")

def safe_pickle_loads(data):
    return RestrictedUnpickler(io.BytesIO(data)).load()
```

### YAML Deserialization

```python
# ❌ Arbitrary code execution
import yaml
data = yaml.load(untrusted_input)  # yaml.load is unsafe

# ✅ Use safe_load
import yaml
data = yaml.safe_load(untrusted_input)  # Only loads safe types

# ✅ Or use full_load with caution
data = yaml.full_load(untrusted_input)  # Better than load()
```

### XML Attacks

```python
# ❌ XML External Entity (XXE) attack
import xml.etree.ElementTree as ET
tree = ET.parse(untrusted_xml)  # Vulnerable to XXE

# ✅ Disable external entities
import defusedxml.ElementTree as ET
tree = ET.parse(untrusted_xml)  # Safe from XXE

# ✅ Or configure parser
from lxml import etree
parser = etree.XMLParser(resolve_entities=False)
tree = etree.parse(untrusted_xml, parser)
```

---

## Command Injection

### os.system and subprocess

```python
# ❌ CRITICAL: Command injection
import os
filename = request.args.get('file')
os.system(f'cat {filename}')  # Attack: file=test.txt; rm -rf /

# ❌ Also vulnerable
import subprocess
subprocess.call(f'cat {filename}', shell=True)

# ✅ Use list form (no shell)
import subprocess
result = subprocess.run(['cat', filename], capture_output=True, text=True)

# ✅ Validate input first
import re
if not re.match(r'^[\w\-. ]+$', filename):
    abort(400, 'Invalid filename')
result = subprocess.run(['cat', filename], capture_output=True, text=True)

# ✅ Use shlex for safe quoting if shell is needed
import shlex
import subprocess
safe_filename = shlex.quote(filename)
subprocess.run(f'cat {safe_filename}', shell=True)
```

---

## Path Traversal

### File Access

```python
# ❌ Directory traversal
import os
filename = request.args.get('file')
with open(f'/uploads/{filename}', 'r') as f:
    content = f.read()
# Attack: file=../../etc/passwd

# ✅ Use os.path.basename to remove directory components
import os
filename = os.path.basename(request.args.get('file'))
filepath = os.path.join('/uploads', filename)

# ✅ Verify path is within allowed directory
import os.path
allowed_dir = os.path.abspath('/uploads')
requested_path = os.path.abspath(filepath)
if not requested_path.startswith(allowed_dir):
    abort(400, 'Invalid path')

with open(requested_path, 'r') as f:
    content = f.read()
```

### Template Injection (Jinja2)

```python
# ❌ CRITICAL: Server-Side Template Injection (SSTI)
from jinja2 import Template
user_input = request.args.get('name')
template = Template(f'Hello {user_input}!')  # Never template user input
output = template.render()
# Attack: {{ config.items() }} or {{ ''.__class__.__mro__[1].__subclasses__() }}

# ✅ Pass user input as variable
from jinja2 import Template
user_input = request.args.get('name')
template = Template('Hello {{ name }}!')
output = template.render(name=user_input)

# ✅ Use Flask's render_template_string safely
from flask import render_template_string
output = render_template_string('Hello {{ name }}!', name=user_input)
```

---

## Cryptography

### Weak Hashing

```python
# ❌ Weak password hashing
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()  # MD5 is broken

# ❌ SHA1 also broken
password_hash = hashlib.sha1(password.encode()).hexdigest()

# ❌ Even SHA256 without salt is weak for passwords
password_hash = hashlib.sha256(password.encode()).hexdigest()

# ✅ Use bcrypt
import bcrypt
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Verify later
if bcrypt.checkpw(password.encode(), password_hash):
    # Password correct
    pass

# ✅ Or use Argon2 (best for new projects)
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)

# Verify later
try:
    ph.verify(password_hash, password)
    # Password correct
except:
    # Password incorrect
    pass
```

### Weak Encryption

```python
# ❌ Hardcoded encryption key
from cryptography.fernet import Fernet
key = b'hardcoded_key_1234567890123456'  # NEVER hardcode
cipher = Fernet(key)

# ✅ Generate and store key securely
import os
from cryptography.fernet import Fernet

# Generate once and store in environment/secrets manager
key = Fernet.generate_key()

# Later: load from environment
key = os.environ['ENCRYPTION_KEY'].encode()
cipher = Fernet(key)

encrypted = cipher.encrypt(plaintext.encode())
```

### Insecure Random

```python
# ❌ Predictable random for security purposes
import random
token = random.randint(100000, 999999)  # Predictable

# ✅ Use secrets module
import secrets
token = secrets.randbelow(900000) + 100000

# ✅ For tokens
token = secrets.token_urlsafe(32)

# ✅ For API keys
api_key = secrets.token_hex(32)
```

---

## Web Framework Security

### Flask

```python
# ✅ Secure Flask configuration
from flask import Flask
import os

app = Flask(__name__)

# Security configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# ❌ NEVER in production
app.config['DEBUG'] = False  # No debug mode in production

# ✅ Security headers
from flask_talisman import Talisman
Talisman(app, force_https=True)

# ✅ CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# ✅ Rate limiting
from flask_limiter import Limiter
limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

### Django

```python
# settings.py

# ✅ Security settings
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False  # Never True in production
ALLOWED_HOSTS = ['example.com']

# Session security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'

# CSRF protection
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ...
]

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### FastAPI

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

app = FastAPI()

# ✅ CORS configuration (restrictive)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],  # Not ["*"]
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ✅ Trusted hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["example.com", "*.example.com"]
)

# ✅ Rate limiting
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/data")
@limiter.limit("5/minute")
async def get_data():
    return {"data": "value"}

# ✅ Input validation with Pydantic
from pydantic import BaseModel, validator

class UserCreate(BaseModel):
    username: str
    email: str
    age: int

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('must be alphanumeric')
        return v

    @validator('age')
    def age_range(cls, v):
        if v < 0 or v > 150:
            raise ValueError('must be between 0 and 150')
        return v
```

---

## Dependencies

### Vulnerable Packages

```bash
# Check for vulnerabilities
pip-audit
safety check
pip install --upgrade pip-audit

# Or use pipenv
pipenv check

# Or use poetry
poetry show --outdated
```

### Common Vulnerable Patterns

```python
# requirements.txt

# ❌ No version pinning
flask
requests

# ❌ Very old versions
Django==1.11.0  # Many known CVEs

# ✅ Pin versions with compatible ranges
Flask>=2.3.0,<3.0.0
requests>=2.31.0,<3.0.0
Django>=4.2.0,<5.0.0

# ✅ Use lock files
# requirements.lock or Pipfile.lock or poetry.lock
```

---

## Configuration

### Environment Variables

```python
# ❌ Hardcoded secrets
DATABASE_URL = 'postgresql://user:password@localhost/db'
API_KEY = 'sk_live_1234567890'

# ✅ Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

DATABASE_URL = os.environ.get('DATABASE_URL')
API_KEY = os.environ.get('API_KEY')

# ✅ Validate required variables
required_vars = ['DATABASE_URL', 'API_KEY', 'SECRET_KEY']
missing = [var for var in required_vars if not os.environ.get(var)]
if missing:
    raise ValueError(f'Missing required environment variables: {missing}')
```

### Debug Mode

```python
# ❌ Debug mode in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # NEVER in production

# ✅ Control via environment
if __name__ == '__main__':
    debug_mode = os.environ.get('DEBUG', 'False') == 'True'
    app.run(debug=debug_mode, host='127.0.0.1')
```

---

## ORM Security

### Django ORM

```python
# ✅ Use ORM methods (parameterized)
User.objects.filter(username=username)

# ❌ Raw SQL with string formatting
User.objects.raw(f"SELECT * FROM users WHERE username = '{username}'")

# ✅ Raw SQL with parameters
User.objects.raw("SELECT * FROM users WHERE username = %s", [username])

# ✅ Extra() with parameters
User.objects.extra(
    where=["username = %s"],
    params=[username]
)
```

### SQLAlchemy

```python
# ✅ ORM methods
from sqlalchemy import select
stmt = select(User).where(User.username == username)
user = session.execute(stmt).scalar_one_or_none()

# ✅ Text with parameters
from sqlalchemy import text
stmt = text("SELECT * FROM users WHERE username = :username")
user = session.execute(stmt, {"username": username}).first()

# ❌ String formatting
stmt = text(f"SELECT * FROM users WHERE username = '{username}'")
```

---

## Type Safety

### Type Hints for Security

```python
# ✅ Use type hints to enforce contracts
from typing import NewType

UserId = NewType('UserId', int)

def get_user(user_id: UserId) -> dict:
    # user_id is guaranteed to be int
    return db.query("SELECT * FROM users WHERE id = ?", (user_id,))

# Usage
user_id = UserId(int(request.args.get('id')))  # Explicit conversion
user = get_user(user_id)
```

### Pydantic for Runtime Validation

```python
from pydantic import BaseModel, EmailStr, validator, conint

class UserCreate(BaseModel):
    username: str
    email: EmailStr  # Validates email format
    age: conint(ge=0, le=150)  # Constrained int
    password: str

    @validator('username')
    def username_valid(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be 3-20 characters')
        return v

    @validator('password')
    def password_strong(cls, v):
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters')
        return v

# Usage
try:
    user_data = UserCreate(**request.json)
    # user_data is validated and type-safe
except ValidationError as e:
    return {'error': e.errors()}, 400
```

---

## Quick Reference

| Vulnerability | Pattern | Mitigation |
|---------------|---------|------------|
| **SQL Injection** | `f"SELECT * FROM users WHERE id={id}"` | Use parameterized queries |
| **Pickle RCE** | `pickle.loads(data)` | Use JSON, or RestrictedUnpickler |
| **Command Injection** | `os.system(f'cmd {input}')` | Use subprocess with list args |
| **Path Traversal** | `open(f'/files/{filename}')` | Use os.path.basename(), validate path |
| **Weak Hashing** | `hashlib.md5(password)` | Use bcrypt or Argon2 |
| **SSTI** | `Template(f'Hello {input}')` | Pass as variable, not in template |
| **XXE** | `ET.parse(xml)` | Use defusedxml |
| **Insecure Random** | `random.randint()` | Use secrets module |
| **Hardcoded Secrets** | `API_KEY = 'sk_live_123'` | Use environment variables |

---

## Security Tools for Python

### Static Analysis

```bash
# Bandit - security linter
pip install bandit
bandit -r /path/to/code

# Semgrep - pattern matching
pip install semgrep
semgrep --config=auto /path/to/code

# Pylint with security plugins
pip install pylint pylint-django
pylint /path/to/code
```

### Dependency Scanning

```bash
# Safety
pip install safety
safety check

# pip-audit
pip install pip-audit
pip-audit
```

---

## References

- [OWASP Python Security](https://owasp.org/www-project-python-security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [Flask Security](https://flask.palletsprojects.com/en/stable/security/)
