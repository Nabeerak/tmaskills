---
name: fastapi-builder
description: |
  Build production-ready REST APIs with FastAPI, including proper project structure,
  CRUD operations, request/response validation with Pydantic, error handling,
  dependency injection, and SQLModel database integration. This skill should be used
  when users ask to create FastAPI applications, build REST APIs, set up API endpoints,
  implement CRUD operations, or integrate FastAPI with databases.
---

# FastAPI Builder

Build production-ready REST APIs with FastAPI following industry best practices.

## What This Skill Does

- Creates FastAPI projects with proper layered architecture
- Implements CRUD endpoints with routing and validation
- Sets up Pydantic models for request/response validation
- Configures error handling and exception patterns
- Implements dependency injection for database sessions, authentication
- Configures CORS middleware for cross-origin requests
- Integrates with SQLModel for database operations
- Generates automatic API documentation (Swagger/ReDoc)

## What This Skill Does NOT Do

- Deploy applications to production servers
- Set up infrastructure (Docker, Kubernetes)
- Implement frontend applications
- Handle real-time WebSocket connections (use dedicated WebSocket patterns)
- Manage database migrations (use Alembic separately)

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing project structure, patterns, conventions, database models |
| **Conversation** | User's specific requirements, API endpoints needed, business logic |
| **Skill References** | FastAPI patterns from `references/` (best practices, examples, anti-patterns) |
| **User Guidelines** | Project-specific conventions, team standards, code style |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER'S specific context:

1. **API Purpose**: "What is the API for?" (e.g., task management, user authentication, e-commerce)
2. **Endpoints Needed**: "What resources/entities need CRUD operations?" (e.g., users, tasks, products)
3. **Database**: "Using SQLModel with which database?" (PostgreSQL, MySQL, SQLite - default to SQLite for development)
4. **Authentication**: "Need authentication?" (None, Basic, JWT, OAuth2 - clarify if not mentioned)
5. **Special Requirements**: "Any specific requirements?" (rate limiting, file uploads, caching, etc.)

**Question Pacing**: Ask 1-2 questions at a time. Infer from context where possible to avoid over-asking.

**If User Doesn't Answer**: Use sensible defaults (SQLite for database, no authentication, standard CRUD patterns) and mention assumptions in implementation.

## Optional Clarifications

Ask if context suggests need:

- **File Uploads**: "Need file upload support?" (affects multipart form handling)
- **Background Tasks**: "Need async background processing?" (email, notifications, etc.)
- **WebSockets**: "Need real-time features?" (affects server setup)
- **API Versioning Strategy**: "Need multiple API versions?" (affects routing structure)
- **Rate Limiting**: "Need rate limiting?" (affects middleware configuration)

---

## Project Structure

Use layered architecture for maintainability and scalability:

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization, middleware, CORS
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings with Pydantic BaseSettings
│   │   └── database.py      # Database connection and session
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   └── [entity].py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── [entity].py
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   ├── deps.py          # Shared dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py       # Main router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           └── [entity].py
│   ├── crud/                # CRUD operations (optional service layer)
│   │   ├── __init__.py
│   │   └── [entity].py
│   └── exceptions/          # Custom exceptions and handlers
│       ├── __init__.py
│       └── handlers.py
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

See `references/project-structure.md` for detailed organization patterns.

---

## Official Documentation

For latest patterns and updates, refer to:

| Resource | URL | Use For |
|----------|-----|---------|
| FastAPI | https://fastapi.tiangolo.com/ | Framework features, advanced patterns |
| Pydantic | https://docs.pydantic.dev/ | Validation, settings, schemas |
| SQLModel | https://sqlmodel.tiangolo.com/ | Database models, relationships |
| Uvicorn | https://www.uvicorn.org/ | Server configuration, deployment |

**Version Compatibility**: Patterns current as of FastAPI 0.109+, Pydantic v2, SQLModel 0.0.14+. Check official docs for latest features.

**For Unlisted Patterns**: When encountering FastAPI features, authentication methods, or database patterns not covered in these references, fetch the latest official documentation from the URLs above.

---

## Implementation Workflow

### 1. Initialize Project

```bash
# Create project directory
mkdir project-name && cd project-name

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install fastapi uvicorn sqlmodel python-dotenv pydantic-settings
pip freeze > requirements.txt
```

**If Dependencies Missing**: Check Python version (3.8+ required). For SQLModel issues, ensure SQLAlchemy 2.0+ is installed. Run `pip install --upgrade pip` if package resolution fails.

### 2. Create Core Configuration

Start with `app/core/config.py` using Pydantic Settings (see `assets/templates/config.py`).

Key settings to include:
- `PROJECT_NAME`: Application name
- `VERSION`: API version
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: For JWT/sessions (if auth needed)
- `CORS_ORIGINS`: Allowed origins list

### 3. Set Up Database Connection

Create `app/core/database.py` for SQLModel engine and session (see `assets/templates/database.py`).

Pattern:
- Create SQLModel engine
- Define `get_session()` dependency with yield
- Handle session lifecycle (commit/rollback)

### 4. Define Models and Schemas

**Models** (`app/models/`): SQLModel classes for database tables
**Schemas** (`app/schemas/`): Pydantic models for API request/response

See `references/models-vs-schemas.md` for the distinction and `assets/templates/` for examples.

### 5. Create CRUD Operations

Implement in `app/crud/` (optional but recommended for complex logic):
- `create()`: Insert new records
- `get()`: Retrieve single record
- `get_multi()`: Retrieve multiple with pagination
- `update()`: Update existing record
- `delete()`: Remove record

See `assets/templates/crud_base.py` for reusable base class.

### 6. Implement API Endpoints

Create routers in `app/api/v1/endpoints/`:
- Use FastAPI `APIRouter`
- Apply dependency injection for database session
- Add Pydantic models for validation
- Include proper HTTP status codes
- Add response models for documentation

See `assets/templates/endpoint_example.py` for complete CRUD endpoint.

### 7. Configure Main Application

In `app/main.py`:
- Initialize FastAPI app with metadata
- Add CORS middleware
- Include API routers
- Register exception handlers
- Add startup/shutdown events (if needed)

See `assets/templates/main.py` for complete setup.

### 8. Add Error Handling

Create custom exceptions and handlers in `app/exceptions/`:
- Define domain-specific exceptions
- Create exception handlers
- Return consistent error response format

See `references/error-handling.md` for patterns.

---

## CRUD Endpoint Pattern

Standard pattern for resource endpoints:

| Operation | HTTP Method | Path | Description |
|-----------|-------------|------|-------------|
| Create | POST | `/api/v1/items` | Create new item |
| Read (list) | GET | `/api/v1/items` | Get all items (with pagination) |
| Read (single) | GET | `/api/v1/items/{id}` | Get specific item |
| Update | PUT/PATCH | `/api/v1/items/{id}` | Update item |
| Delete | DELETE | `/api/v1/items/{id}` | Delete item |

See `references/crud-patterns.md` for detailed implementation patterns.

---

## Dependency Injection

Common dependencies to create in `app/api/deps.py`:

1. **Database Session**: `get_session()` - Yields database session with cleanup
2. **Current User**: `get_current_user()` - Validates auth token, returns user
3. **Pagination**: `CommonQueryParams` - Reusable skip/limit parameters
4. **Permissions**: `require_admin()` - Role-based access control

See `references/dependency-injection.md` for advanced patterns.

---

## Validation and Serialization

### Request Validation
- Use Pydantic `Field()` for constraints (min/max, regex, etc.)
- Create separate schemas for Create/Update operations
- Use `validator` decorator for custom validation logic

### Response Models
- Define with `response_model` parameter on routes
- Use `response_model_exclude_none` to omit null fields
- Create separate response schemas (exclude sensitive fields)

See `references/validation-patterns.md` for examples.

---

## CORS Configuration

Add CORS middleware in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Load from environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Security Notes**:
- Never use `allow_origins=["*"]` with `allow_credentials=True`
- Specify exact origins in production
- Load origins from environment variables

See `references/cors-security.md` for details.

---

## Standards to Follow

### Must Follow
- [ ] Use type hints for all function parameters and returns
- [ ] Validate all inputs with Pydantic models
- [ ] Use dependency injection for database sessions
- [ ] Return appropriate HTTP status codes (201 for create, 204 for delete, etc.)
- [ ] Include proper error handling with consistent error responses
- [ ] Use async/await for I/O-bound operations
- [ ] Add docstrings to routes for auto-generated documentation
- [ ] Separate models (database) from schemas (API)
- [ ] Use environment variables for configuration (never hardcode secrets)
- [ ] Implement pagination for list endpoints
- [ ] Hash passwords with bcrypt (never store plain text)
- [ ] Use parameterized queries (SQLModel handles this automatically)
- [ ] Enforce HTTPS in production
- [ ] Implement rate limiting for public endpoints
- [ ] Handle database connection failures gracefully
- [ ] Validate file upload size limits (if file uploads supported)
- [ ] Handle pagination edge cases (empty results, invalid skip/limit)
- [ ] Consider concurrent updates (optimistic locking for critical operations)

### Must Avoid
- [ ] Don't use mutable defaults in function parameters
- [ ] Don't expose database models directly in API responses
- [ ] Don't commit database sessions in route handlers (use dependencies)
- [ ] Don't ignore exception handling (always handle database/validation errors)
- [ ] Don't use synchronous database operations (use async with SQLModel)
- [ ] Don't hardcode CORS origins to `["*"]` in production
- [ ] Don't skip request validation (always use Pydantic models)
- [ ] Don't return 200 for all responses (use correct status codes)

See `references/anti-patterns.md` for common mistakes to avoid.

---

## Running the Application

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Output Checklist

Before delivering, verify:

**Project Structure**
- [ ] Follows layered architecture (core, models, schemas, api, crud)
- [ ] Configuration loaded from environment variables
- [ ] Database connection properly configured with session management

**API Implementation**
- [ ] All requested endpoints implemented with proper HTTP methods
- [ ] Request validation with Pydantic schemas
- [ ] Response models defined and used
- [ ] Proper HTTP status codes returned

**Code Quality**
- [ ] Type hints on all functions
- [ ] Async/await used for database operations
- [ ] Error handling implemented with custom exceptions
- [ ] Dependency injection for database session and auth

**Security**
- [ ] CORS properly configured (not using wildcard with credentials)
- [ ] Sensitive data not exposed in responses
- [ ] Environment variables used for secrets
- [ ] Input validation on all endpoints

**Documentation**
- [ ] Route docstrings for Swagger documentation
- [ ] README with setup and run instructions
- [ ] .env.example provided
- [ ] API documentation accessible at /docs

**Testing Ready**
- [ ] Code structure supports easy testing
- [ ] Dependencies can be mocked
- [ ] Database session uses dependency injection
- [ ] Use `/pytest-tdd` skill for comprehensive test implementation
- [ ] Target 80%+ code coverage on critical paths

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/project-structure.md` | Detailed project organization patterns |
| `references/models-vs-schemas.md` | Understanding SQLModel models vs Pydantic schemas |
| `references/crud-patterns.md` | Complete CRUD implementation examples |
| `references/dependency-injection.md` | Advanced dependency patterns |
| `references/validation-patterns.md` | Pydantic validation examples |
| `references/error-handling.md` | Exception handling and custom errors |
| `references/cors-security.md` | CORS configuration and security |
| `references/anti-patterns.md` | Common mistakes to avoid |
| `references/best-practices.md` | Production-ready patterns and tips |

**Finding Specific Topics**: All reference files include a table of contents. For quick searches across all references, use these grep patterns:

```bash
# Error handling patterns
grep -r "HTTPException\|raise\|try.*except" references/

# Validation patterns
grep -r "@field_validator\|@model_validator\|Field(" references/

# Security patterns
grep -r "CORS\|SECRET_KEY\|password\|hash\|token" references/

# Database patterns
grep -r "Session\|select\|commit\|rollback\|query" references/

# Dependency injection
grep -r "Depends\|dependency\|get_session" references/

# Authentication
grep -r "auth\|JWT\|OAuth\|Bearer" references/

# Async patterns
grep -r "async\|await\|AsyncSession" references/
```

---

## Assets

| File | Purpose |
|------|---------|
| `assets/templates/config.py` | Pydantic Settings configuration |
| `assets/templates/database.py` | SQLModel database setup |
| `assets/templates/main.py` | FastAPI application initialization |
| `assets/templates/crud_base.py` | Reusable CRUD base class |
| `assets/templates/endpoint_example.py` | Complete CRUD endpoint example |
| `assets/templates/model_example.py` | SQLModel model template |
| `assets/templates/schema_example.py` | Pydantic schema templates |
