# FastAPI Best Practices

Production-ready patterns and recommendations for building robust FastAPI applications.

## Table of Contents

- [Project Organization](#project-organization)
- [Configuration Management](#configuration-management)
- [Database Best Practices](#database-best-practices)
- [API Design](#api-design)
- [Security](#security)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Performance](#performance)
- [Documentation](#documentation)
- [Code Quality](#code-quality)
- [Deployment](#deployment)
- [Summary Checklist](#summary-checklist)

---

## Project Organization

### Use Layered Architecture

```
app/
├── core/         # Configuration, database, security
├── models/       # Database models
├── schemas/      # Request/response models
├── api/          # API routes
├── crud/         # Business logic (optional)
└── exceptions/   # Custom exceptions
```

**Benefits**:
- Clear separation of concerns
- Easy to test
- Scalable as project grows

---

## Configuration Management

### Use Pydantic Settings

```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "My API"
    VERSION: str = "1.0.0"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Cache settings (loaded once)."""
    return Settings()

# Usage
settings = get_settings()
```

**Benefits**:
- Type-safe configuration
- Environment variable support
- Automatic validation
- Easy to test (override settings)

---

## Database Best Practices

### 1. Use Dependency Injection for Sessions

```python
def get_session():
    with Session(engine) as session:
        yield session

@router.get("/tasks")
def get_tasks(session: Session = Depends(get_session)):
    ...
```

### 2. Use Context Managers

```python
# ✅ Automatic cleanup
with Session(engine) as session:
    task = session.get(Task, task_id)

# ❌ Manual cleanup needed
session = Session(engine)
task = session.get(Task, task_id)
session.close()  # Easy to forget!
```

### 3. Handle Transactions Properly

```python
try:
    session.add(task)
    session.add(notification)
    session.commit()
except IntegrityError:
    session.rollback()
    raise HTTPException(status_code=409, detail="Duplicate entry")
```

### 4. Use Indexes on Frequent Queries

```python
class User(SQLModel, table=True):
    email: str = Field(unique=True, index=True)  # Index for lookups
    username: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
```

---

## API Design

### 1. Use Proper HTTP Methods

| Method | Usage | Example |
|--------|-------|---------|
| GET | Retrieve resources | `GET /tasks` |
| POST | Create resources | `POST /tasks` |
| PUT | Full update | `PUT /tasks/1` |
| PATCH | Partial update | `PATCH /tasks/1` |
| DELETE | Delete resources | `DELETE /tasks/1` |

### 2. Use Proper Status Codes

```python
@router.post("/tasks", status_code=status.HTTP_201_CREATED)  # Create
@router.get("/tasks")  # Read - 200 OK (default)
@router.patch("/tasks/{id}")  # Update - 200 OK
@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)  # Delete
```

### 3. Version Your API

```python
# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import tasks, users

api_router = APIRouter()
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# app/main.py
app.include_router(api_router, prefix="/api/v1")

# URLs: /api/v1/tasks, /api/v1/users
```

### 4. Implement Pagination

```python
class CommonQueryParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000)
    ):
        self.skip = skip
        self.limit = limit

@router.get("/tasks")
def get_tasks(
    commons: CommonQueryParams = Depends(),
    session: Session = Depends(get_session)
):
    statement = select(Task).offset(commons.skip).limit(commons.limit)
    return session.exec(statement).all()
```

---

## Security

### 1. Never Hardcode Secrets

```python
# ❌ Bad
SECRET_KEY = "my-secret-123"

# ✅ Good
SECRET_KEY = os.getenv("SECRET_KEY")
# or
SECRET_KEY: str  # From Pydantic Settings
```

### 2. Hash Passwords

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### 3. Use HTTPS in Production

```python
# Force HTTPS
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if settings.ENVIRONMENT == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

### 4. Implement Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.get("/tasks")
@limiter.limit("100/minute")
def get_tasks(request: Request):
    ...
```

### 5. Validate All Inputs

```python
# Use Pydantic models for validation
@router.post("/tasks")
def create_task(task_in: TaskCreate):  # Validated automatically
    ...

# Add extra validation
@router.get("/tasks/{task_id}")
def get_task(task_id: int = Path(..., gt=0)):  # Must be positive
    ...
```

---

## Error Handling

### 1. Use Custom Exceptions

```python
class NotFoundException(Exception):
    def __init__(self, resource: str, id: int):
        self.resource = resource
        self.id = id

@app.exception_handler(NotFoundException)
async def not_found_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.resource} {exc.id} not found"}
    )
```

### 2. Return Consistent Error Format

```json
{
  "error": "ErrorType",
  "message": "Human-readable message",
  "details": {...},  // Optional
  "path": "/api/v1/tasks/123"
}
```

### 3. Log Errors

```python
import logging

logger = logging.getLogger(__name__)

try:
    process_task(task)
except Exception as e:
    logger.error(f"Failed to process task {task.id}", exc_info=True)
    raise HTTPException(status_code=500, detail="Processing failed")
```

---

## Testing

### 1. Use TestClient

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_task():
    response = client.post("/api/v1/tasks", json={"title": "Test"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test"
```

### 2. Override Dependencies

```python
def override_get_session():
    with Session(test_engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session
```

### 3. Use Fixtures

```python
import pytest

@pytest.fixture
def test_user():
    return User(id=1, email="test@example.com", username="testuser")

def test_get_user(test_user):
    ...
```

---

## Performance

### 1. Use Async for I/O Operations

```python
# ✅ Async for I/O
@router.get("/tasks")
async def get_tasks():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/tasks")
    return response.json()

# ✅ Sync for CPU-bound
@router.post("/process")
def process_data(data: ProcessInput):
    result = cpu_intensive_calculation(data)
    return result
```

### 2. Use Background Tasks

```python
from fastapi import BackgroundTasks

def send_notification(email: str):
    # Send email (slow operation)
    ...

@router.post("/tasks")
def create_task(
    task_in: TaskCreate,
    background_tasks: BackgroundTasks
):
    task = create_task_logic(task_in)

    # Don't block response
    background_tasks.add_task(send_notification, task.user.email)

    return task
```

### 3. Cache Expensive Operations

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_expensive_computation(param: int) -> dict:
    # Expensive operation
    return result

# Or use Redis
from redis import Redis

redis = Redis()

def get_user(user_id: int):
    cached = redis.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    user = fetch_user_from_db(user_id)
    redis.setex(f"user:{user_id}", 3600, json.dumps(user))
    return user
```

### 4. Use Database Query Optimization

```python
# ❌ N+1 query problem
tasks = session.exec(select(Task)).all()
for task in tasks:
    user = task.user  # Separate query for each task!

# ✅ Eager loading
from sqlmodel import selectinload

statement = select(Task).options(selectinload(Task.user))
tasks = session.exec(statement).all()
for task in tasks:
    user = task.user  # Already loaded!
```

---

## Documentation

### 1. Add Docstrings

```python
@router.post("/tasks", response_model=TaskResponse)
def create_task(task_in: TaskCreate):
    """
    Create a new task.

    - **title**: Task title (required, max 100 chars)
    - **description**: Detailed description (optional)
    - **priority**: Priority 1-5 (default: 3)

    Returns the created task with generated ID.
    """
    ...
```

### 2. Use Field Descriptions

```python
class TaskCreate(BaseModel):
    title: str = Field(..., max_length=100, description="Task title")
    description: str | None = Field(None, description="Detailed description")
    priority: int = Field(3, ge=1, le=5, description="Priority level (1-5)")
```

### 3. Add Response Examples

```python
class Config:
    json_schema_extra = {
        "example": {
            "title": "Complete project",
            "description": "Finish the project by Friday",
            "priority": 4
        }
    }
```

### 4. Customize OpenAPI Metadata

```python
app = FastAPI(
    title="Task Management API",
    description="API for managing tasks and projects",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)
```

---

## Code Quality

### 1. Use Type Hints Everywhere

```python
def get_task(task_id: int, session: Session) -> Task | None:
    return session.get(Task, task_id)
```

### 2. Use Linting and Formatting

```bash
# Install tools
pip install black ruff mypy

# Format code
black app/

# Lint code
ruff check app/

# Type check
mypy app/
```

### 3. Write Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run tests with coverage
pytest --cov=app tests/
```

### 4. Use Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.261
    hooks:
      - id: ruff
```

---

## Deployment

### 1. Use Environment Variables

```bash
# .env (development)
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=dev-secret-key
ENVIRONMENT=development

# Production (set in server)
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=generated-production-key
ENVIRONMENT=production
```

### 2. Use Proper Logging

```python
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### 3. Use Health Check Endpoint

```python
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }
```

### 4. Use Proper Server Configuration

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production (with gunicorn)
gunicorn app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile -
```

---

## Summary Checklist

Production-ready API checklist:

**Structure**
- [ ] Layered architecture (core, models, schemas, api)
- [ ] Separate models from schemas
- [ ] Use dependency injection

**Configuration**
- [ ] Environment variables for config
- [ ] No hardcoded secrets
- [ ] Pydantic Settings for type safety

**Security**
- [ ] HTTPS in production
- [ ] Password hashing
- [ ] CORS properly configured
- [ ] Input validation on all endpoints
- [ ] Rate limiting

**API Design**
- [ ] Proper HTTP methods and status codes
- [ ] API versioning
- [ ] Pagination on list endpoints
- [ ] Consistent error responses

**Code Quality**
- [ ] Type hints everywhere
- [ ] Linting and formatting
- [ ] Tests with good coverage
- [ ] Pre-commit hooks

**Documentation**
- [ ] Docstrings on all endpoints
- [ ] Field descriptions
- [ ] OpenAPI metadata
- [ ] README with setup instructions

**Performance**
- [ ] Async for I/O operations
- [ ] Background tasks for slow operations
- [ ] Database query optimization
- [ ] Caching where appropriate

**Operations**
- [ ] Proper logging
- [ ] Health check endpoint
- [ ] Error tracking (Sentry)
- [ ] Monitoring (Prometheus/Grafana)
