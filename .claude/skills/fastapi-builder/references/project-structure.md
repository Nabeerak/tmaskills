# FastAPI Project Structure Patterns

## Table of Contents

- [Layered Architecture (Recommended)](#layered-architecture-recommended)
- [Detailed Directory Structure](#detailed-directory-structure)
- [Alternative Structures](#alternative-structures)
- [Best Practices](#best-practices)
- [Migration Path](#migration-path)

---

## Layered Architecture (Recommended)

The layered architecture separates concerns into distinct layers, making the codebase maintainable, testable, and scalable.

### Three-Tier Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── core/                # Core functionality (config, database, security)
│   ├── models/              # Database models (SQLModel)
│   ├── schemas/             # Pydantic request/response schemas
│   ├── api/                 # API routes and endpoints
│   ├── crud/                # CRUD operations (optional service layer)
│   └── exceptions/          # Custom exceptions and handlers
├── tests/
├── .env
├── .env.example
└── requirements.txt
```

### Layer Responsibilities

| Layer | Responsibility | Files |
|-------|---------------|-------|
| **API Layer** | Handle HTTP requests/responses | `api/v1/endpoints/` |
| **Business Logic** | Implement business rules | `crud/` (service layer) |
| **Data Access** | Database operations | `models/`, database session |
| **Core Services** | Shared functionality | `core/config.py`, `core/database.py` |

---

## Detailed Directory Structure

### Core Directory (`app/core/`)

Contains application-wide configuration and initialization.

```
core/
├── __init__.py
├── config.py        # Application settings (Pydantic BaseSettings)
├── database.py      # Database engine and session management
└── security.py      # Authentication/authorization utilities (optional)
```

**When to add files**:
- `security.py`: When implementing JWT/OAuth2 authentication
- `logging.py`: For centralized logging configuration
- `cache.py`: For Redis or in-memory caching setup

### Models Directory (`app/models/`)

SQLModel classes representing database tables.

```
models/
├── __init__.py
├── user.py          # User model with relationships
├── task.py          # Task model
└── base.py          # Base model with common fields (optional)
```

**Pattern**: One file per entity. Import all models in `__init__.py` for easy access.

### Schemas Directory (`app/schemas/`)

Pydantic models for API request/response validation.

```
schemas/
├── __init__.py
├── user.py          # UserCreate, UserUpdate, UserResponse
├── task.py          # TaskCreate, TaskUpdate, TaskResponse
└── common.py        # Shared schemas (Pagination, Message, etc.)
```

**Pattern**: Create separate schemas for Create, Update, and Response operations.

### API Directory (`app/api/`)

API routes organized by version and endpoints.

```
api/
├── __init__.py
├── deps.py          # Shared dependencies (get_session, get_current_user)
└── v1/
    ├── __init__.py
    ├── api.py       # Main API router combining all endpoints
    └── endpoints/
        ├── __init__.py
        ├── users.py
        └── tasks.py
```

**Versioning**: Use `/api/v1/` prefix for version 1. When breaking changes needed, create `v2/`.

### CRUD Directory (`app/crud/`)

Optional service layer for complex business logic.

```
crud/
├── __init__.py
├── base.py          # Generic CRUD base class
├── user.py          # User-specific CRUD operations
└── task.py          # Task-specific CRUD operations
```

**When to use**: For complex business logic, transactions, or when separating data access from endpoints.

### Exceptions Directory (`app/exceptions/`)

Custom exceptions and global exception handlers.

```
exceptions/
├── __init__.py
├── custom.py        # Custom exception classes
└── handlers.py      # Exception handlers for FastAPI
```

---

## Alternative Structures

### Microservice Structure (Single Domain)

For smaller services focused on one domain:

```
project/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routes.py
└── tests/
```

**When to use**: Small services with <5 endpoints, single domain.

### Domain-Driven Design (Multiple Domains)

For larger applications with multiple bounded contexts:

```
project/
├── app/
│   ├── main.py
│   ├── core/
│   ├── users/              # User domain
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   └── services.py
│   ├── tasks/              # Task domain
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── routes.py
│   │   └── services.py
│   └── shared/             # Shared utilities
└── tests/
```

**When to use**: Large applications with clear domain boundaries, multiple teams.

---

## Best Practices

### Naming Conventions

- **Files**: lowercase with underscores (`user_routes.py`)
- **Classes**: PascalCase (`UserCreate`, `TaskResponse`)
- **Functions**: snake_case (`get_user_by_id`, `create_task`)
- **Constants**: UPPERCASE (`DATABASE_URL`, `SECRET_KEY`)

### Import Organization

Order imports in files:
1. Standard library imports
2. Third-party imports (FastAPI, SQLModel, etc.)
3. Local application imports (from `app.models`, `app.schemas`, etc.)

### Configuration Management

- Use `.env` files for environment-specific settings
- Never commit `.env` to version control
- Provide `.env.example` with dummy values
- Use Pydantic `BaseSettings` for type-safe config

### Testing Structure

Mirror the application structure in tests:

```
tests/
├── conftest.py              # Shared fixtures
├── test_main.py
├── api/
│   └── v1/
│       └── test_users.py
└── crud/
    └── test_user.py
```

---

## Migration Path

### From Flat to Layered

If starting with flat structure and need to scale:

1. Create `core/` and move `config.py`, `database.py`
2. Create `models/` and move database models
3. Create `schemas/` and separate from models
4. Create `api/` and organize routes by version
5. Create `crud/` if business logic is complex

### Adding Features

When adding new features, decide placement:
- **New endpoint**: Add to `api/v1/endpoints/`
- **New entity**: Add model, schema, CRUD, endpoint
- **Shared utility**: Add to `core/` or create `utils/`
- **Background task**: Create `workers/` or `tasks/`
