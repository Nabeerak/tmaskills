---
name: sqlmodel-database
description: |
  Design and implement database schemas with SQLModel including model definitions,
  relationships (one-to-many, many-to-many), CRUD operations, complex queries with joins,
  migrations with Alembic, and FastAPI integration. This skill should be used when users
  ask to create database models, set up relationships, implement CRUD operations, write
  queries, configure database migrations, or integrate SQLModel with FastAPI applications.
---

# SQLModel Database

Design production-ready database schemas with SQLModel following best practices for data modeling and FastAPI integration.

## What This Skill Does

- Defines SQLModel database models with proper field types and constraints
- Creates relationships between models (one-to-one, one-to-many, many-to-many)
- Sets up database connections and session management
- Implements CRUD operations (Create, Read, Update, Delete)
- Writes efficient queries with filtering, joins, and aggregations
- Configures database migrations with Alembic
- Integrates SQLModel with FastAPI for API development
- Handles transactions and data integrity

## What This Skill Does NOT Do

- Design database infrastructure (clustering, replication, sharding)
- Optimize database server configuration
- Handle NoSQL databases (MongoDB, Redis, etc.)
- Implement real-time database sync or replication
- Manage database backups and disaster recovery

## Requirements

**Core**: SQLModel 0.0.14+, SQLAlchemy 2.0+, Alembic 1.13+ (migrations)

**Optional**: FastAPI 0.109+ (API), psycopg2-binary (PostgreSQL), pymysql (MySQL), pytest (testing with `/pytest-tdd`)

```bash
pip install sqlmodel alembic  # Core
pip install fastapi uvicorn   # + FastAPI
pip install psycopg2-binary   # + PostgreSQL
```

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, database schema, migration history, connection patterns |
| **Conversation** | Data requirements, relationships, business rules, performance needs |
| **Skill References** | SQLModel patterns from `references/` (models, relationships, queries) |
| **User Guidelines** | Team database standards, naming conventions, migration policies |

### Codebase Scanning Checklist

Scan for project-specific database patterns:

**Models**: Check existing model files (`models/`, `app/models.py`) for field naming (snake_case vs camelCase), relationship naming, primary key patterns (auto-increment vs UUID).

**Configuration**: Read database setup (database.py, config.py) for URL format, connection pool settings, session management (dependency injection vs context managers).

**Migrations**: Review `migrations/` or `alembic/` directory for naming conventions, rollback patterns, data migration approaches.

**Schema**: Note table naming (singular/plural), index naming, constraint prefixes (fk_, idx_, uq_), audit fields (created_at, updated_at).

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

---

## Required Clarifications

Ask about USER'S specific context:

1. **Data Entities**: "What entities/tables do you need?" (e.g., users, products, orders)
2. **Relationships**: "How are entities related?" (one-to-many, many-to-many)
3. **Database Backend**: "Which database?" (PostgreSQL, MySQL, SQLite - default to SQLite for development)
4. **Existing Schema**: "Is there an existing database?" (determines migration strategy)
5. **FastAPI Integration**: "Integrating with FastAPI?" (affects model patterns and dependencies)

**Question Pacing**: Ask 1-2 questions at a time. Infer from context where possible to avoid over-asking.

**If User Doesn't Answer**: Use sensible defaults (SQLite, standard relationships, basic CRUD) and mention assumptions in implementation.

## Optional Clarifications

Ask if context suggests need:

- **Soft Deletes**: "Need soft delete functionality?" (affects model design)
- **Timestamps**: "Need created/updated timestamps?" (adds audit fields)
- **Multi-Tenancy**: "Multiple tenants/organizations?" (affects schema design)
- **Full-Text Search**: "Need full-text search?" (affects indexing strategy)
- **Data Validation**: "Special validation rules?" (custom validators)

---

## Model Definition

Define database models with type-safe fields:

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    username: str = Field(unique=True, index=True, max_length=100)
    full_name: str = Field(max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Key**: Use type hints, add constraints with `Field()` (unique, index, max_length, gt, ge), use `Optional[int]` for auto-increment PKs, add audit fields.

See `references/models.md` for comprehensive patterns including constraints, enums, and JSON fields.

---

## Relationships

Define relationships between models:

```python
from sqlmodel import Relationship
from typing import List, Optional

# One-to-Many
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")

# Many-to-Many (requires link table)
class Link(SQLModel, table=True):
    student_id: int = Field(foreign_key="student.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    courses: List["Course"] = Relationship(back_populates="students", link_model=Link)
```

**Key**: Always use `back_populates`, define foreign keys explicitly, use link tables for many-to-many.

See `references/relationships.md` for one-to-one and self-referential patterns.

---

## Database Connection

Set up database engine and session management:

```python
from sqlmodel import create_engine, Session, SQLModel

DATABASE_URL = "sqlite:///./app.db"  # or postgresql://...
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True, pool_size=10)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():  # FastAPI dependency
    with Session(engine) as session:
        yield session
```

See `references/database-setup.md` for PostgreSQL, MySQL, and connection pooling.

---

## CRUD Operations

Implement Create, Read, Update, Delete operations:

```python
from sqlmodel import select, Session

# Create
def create_user(session: Session, user_data: dict) -> User:
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Read
def get_user(session: Session, user_id: int):
    return session.get(User, user_id)

def get_users(session: Session, skip: int = 0, limit: int = 100):
    return session.exec(select(User).offset(skip).limit(limit)).all()

# Update
def update_user(session: Session, user_id: int, update_data: dict):
    user = session.get(User, user_id)
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
        session.add(user)
        session.commit()
        session.refresh(user)
    return user

# Delete
def delete_user(session: Session, user_id: int):
    if user := session.get(User, user_id):
        session.delete(user)
        session.commit()
        return True
    return False
```

See `references/crud-operations.md` for batch operations and generic CRUD classes.

---

## Queries

Write efficient queries with filtering, joins, and aggregations:

```python
from sqlmodel import select, func

# Filtering
users = session.exec(select(User).where(User.is_active == True, User.age > 18)).all()

# Joins and aggregations
statement = select(User.email, func.count(Post.id)).join(Post).group_by(User.id)
results = session.exec(statement).all()
```

See `references/queries.md` for pagination, OR conditions, LIKE queries, and subqueries.

---

## Migrations with Alembic

Manage database schema changes:

```bash
pip install alembic && alembic init migrations
alembic revision --autogenerate -m "Add tables"
alembic upgrade head  # Apply
alembic downgrade -1  # Rollback
```

**Configure env.py**: Import ALL models, set `target_metadata = SQLModel.metadata`.

**Best Practices**: Review auto-generated migrations, test on dev first, create reversible migrations.

See `references/migrations.md` for configuration and data migrations.

---

## FastAPI Integration

Integrate SQLModel with FastAPI:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session

@app.post("/users", response_model=User, status_code=201)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    if not (user := session.get(User, user_id)):
        raise HTTPException(status_code=404, detail="Not found")
    return user
```

See `references/fastapi-integration.md` for separate read/write models and error handling.

---

## Error Handling & Debugging

Handle common database errors:

**Common Errors**:
- **IntegrityError**: Constraint violation (unique, foreign key) → Use try/except, rollback transaction
- **OperationalError**: Connection/query timeout → Check connection pool and database status
- **InvalidRequestError**: Session state error → Use context managers properly
- **DataError**: Type mismatch/invalid value → Validate data before operations

**Transaction Rollback Pattern**:
```python
from sqlalchemy.exc import IntegrityError
try:
    session.add(user)
    session.commit()
except IntegrityError:
    session.rollback()
    raise HTTPException(status_code=400, detail="Already exists")
```

**Migration Debugging**: Failed migrations → `alembic downgrade -1`, fix errors, reapply. Migration conflicts → Pull latest, merge, regenerate. Enable SQL logging: `echo=True` in create_engine.

---

## Edge Case Testing

Test database edge cases: Null/None values, constraint violations (unique, foreign key), transaction rollbacks, empty results, concurrent updates.

```python
import pytest
from sqlalchemy.exc import IntegrityError

def test_unique_constraint(session):
    session.add(User(email="test@ex.com", username="test"))
    session.commit()
    session.add(User(email="test@ex.com", username="test2"))
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
```

Use `/pytest-tdd` skill for comprehensive database testing.

---

## Official Documentation

For latest patterns and updates, refer to:

| Resource | URL | Use For |
|----------|-----|---------|
| SQLModel | https://sqlmodel.tiangolo.com/ | Core framework, models, relationships |
| SQLAlchemy | https://docs.sqlalchemy.org/ | Advanced queries, migrations |
| Alembic | https://alembic.sqlalchemy.org/ | Database migrations |
| FastAPI + SQLModel | https://fastapi.tiangolo.com/tutorial/sql-databases/ | Integration patterns |

**Version Compatibility**: Patterns current as of SQLModel 0.0.14+, SQLAlchemy 2.0+, Alembic 1.13+. Check official docs for latest features.

**For Unlisted Patterns**: When encountering SQLModel features, relationship patterns, or query techniques not covered in these references, fetch the latest official documentation from the URLs above.

---

## Standards to Follow

### Must Follow
- [ ] Use type hints for all model fields
- [ ] Define relationships with back_populates for bidirectional links
- [ ] Add indexes on frequently queried fields
- [ ] Use session context managers for proper cleanup
- [ ] Commit transactions only after validation succeeds
- [ ] Use Field() for constraints (unique, index, max_length)
- [ ] Define foreign key constraints properly
- [ ] Use meaningful model and field names
- [ ] Add created_at/updated_at timestamps for audit
- [ ] Review and test migrations before applying to production
- [ ] Hash passwords with bcrypt (never store plain text)
- [ ] Use SQLModel's parameterized queries (SQL injection protection built-in)
- [ ] Encrypt sensitive data at rest (e.g., SSN, credit cards)
- [ ] Exclude sensitive fields from API response models
- [ ] Handle constraint violations with proper error messages
- [ ] Validate null/None values before database operations
- [ ] Use try/except for transaction rollback on errors
- [ ] Configure connection pool size and timeouts appropriately

### Must Avoid
- [ ] Don't use mutable defaults in model fields
- [ ] Don't commit inside loops (batch operations instead)
- [ ] Don't ignore database constraints (let database enforce)
- [ ] Don't use string-based queries (use SQLModel select)
- [ ] Don't expose database models directly in API (use schemas)
- [ ] Don't forget to close sessions (use context managers)
- [ ] Don't cascade deletes without careful consideration
- [ ] Don't store sensitive data unencrypted
- [ ] Don't skip migration testing
- [ ] Don't create N+1 query problems (use joins/eager loading)

See `references/best-practices.md` and `references/anti-patterns.md` for detailed guidance.

---

## Output Checklist

Before delivering, verify:

**Model Design**
- [ ] All models defined with proper field types
- [ ] Relationships configured with back_populates
- [ ] Indexes added on frequently queried fields
- [ ] Constraints defined (unique, check, foreign key)
- [ ] Audit fields included (created_at, updated_at) if needed

**Database Setup**
- [ ] Engine configured with appropriate database URL
- [ ] Connection pooling configured for production
- [ ] Session management with dependency injection
- [ ] Database tables created or migrations applied

**CRUD Operations**
- [ ] Create, Read, Update, Delete operations implemented
- [ ] Proper error handling for not found cases
- [ ] Transactions committed only after validation
- [ ] Sessions closed properly with context managers

**Queries**
- [ ] Efficient queries with appropriate filters
- [ ] Joins used instead of N+1 queries
- [ ] Pagination implemented for list endpoints
- [ ] Aggregations used where appropriate

**Migrations**
- [ ] Alembic initialized and configured
- [ ] Migrations generated for all model changes
- [ ] Migrations tested on development database
- [ ] Migration rollback tested

**Integration**
- [ ] FastAPI endpoints use dependency injection for sessions
- [ ] Response models separate from database models
- [ ] Proper HTTP status codes returned
- [ ] Error handling with appropriate exceptions

**Testing**
- [ ] Database models tested with pytest
- [ ] CRUD operations have test coverage
- [ ] Use `/pytest-tdd` skill for comprehensive database testing
- [ ] Target 80%+ code coverage on database operations
- [ ] Test constraint violations (unique, foreign key)

**Standards Verification**
- [ ] All "Must Follow" items from Standards to Follow section verified
- [ ] All "Must Avoid" anti-patterns checked and confirmed absent
- [ ] Edge cases tested (null values, constraint violations, transaction rollbacks)
- [ ] Security checks: Passwords hashed, sensitive data encrypted, response models exclude secrets
- [ ] Error handling: Try/except for transactions, proper constraint violation messages
- [ ] Codebase scanning completed (naming conventions, migration patterns matched)

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/models.md` | Model definition patterns and field types |
| `references/relationships.md` | One-to-many, many-to-many, self-referential relationships |
| `references/database-setup.md` | Engine configuration and session management |
| `references/crud-operations.md` | Complete CRUD patterns with transactions |
| `references/queries.md` | Filtering, joins, aggregations, pagination |
| `references/migrations.md` | Alembic setup and migration patterns |
| `references/fastapi-integration.md` | Integrating SQLModel with FastAPI |
| `references/best-practices.md` | Production-ready patterns and tips |
| `references/anti-patterns.md` | Common mistakes to avoid |

**Finding Specific Topics**: All reference files include a table of contents. For quick searches across all references, use these grep patterns:

```bash
# Model definitions
grep -r "SQLModel.*table=True\|Field(\|Relationship(" references/

# Relationships
grep -r "back_populates\|foreign_key\|link_model" references/

# Queries
grep -r "select(\|where(\|join(\|group_by(" references/

# Migrations
grep -r "alembic\|revision\|upgrade\|downgrade" references/

# CRUD operations
grep -r "session.add\|session.commit\|session.delete" references/

# FastAPI integration
grep -r "Depends\|get_session\|response_model" references/

# Indexes and constraints
grep -r "index=True\|unique=True\|CheckConstraint" references/
```

---

## Assets

| File | Purpose |
|------|---------|
| `assets/templates/models.py` | Example models with relationships |
| `assets/templates/database.py` | Database engine and session setup |
| `assets/templates/crud.py` | CRUD operations template |
| `assets/templates/alembic.ini` | Alembic configuration |
| `assets/templates/env.py` | Alembic env.py template |
