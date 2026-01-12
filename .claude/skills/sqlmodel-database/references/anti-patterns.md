# SQLModel Anti-Patterns

## Table of Contents

- [Model Design Anti-Patterns](#model-design-anti-patterns)
- [Query Anti-Patterns](#query-anti-patterns)
- [Session Management Anti-Patterns](#session-management-anti-patterns)
- [Relationship Anti-Patterns](#relationship-anti-patterns)
- [Migration Anti-Patterns](#migration-anti-patterns)
- [Security Anti-Patterns](#security-anti-patterns)

---

## Model Design Anti-Patterns

### Mutable Defaults

```python
# ❌ Bad
class User(SQLModel, table=True):
    tags: list = []  # Shared across all instances!

# ✓ Good
tags: list = Field(default_factory=list)
```

### Missing Type Hints

```python
# ❌ Bad
email = Field(unique=True)

# ✓ Good
email: str = Field(unique=True)
```

### Exposing Database Models in API

```python
# ❌ Bad
@app.get("/users")
def get_users() -> List[User]:
    return session.exec(select(User)).all()  # Exposes all fields!

# ✓ Good
class UserResponse(BaseModel):
    id: int
    email: str
    # hashed_password excluded

@app.get("/users")
def get_users() -> List[UserResponse]:
    ...
```

---

## Query Anti-Patterns

### N+1 Query Problem

```python
# ❌ Bad
users = session.exec(select(User)).all()
for user in users:
    posts = user.posts  # Separate query for each user!

# ✓ Good
from sqlalchemy.orm import selectinload

users = session.exec(
    select(User).options(selectinload(User.posts))
).all()
```

### Fetching All Records

```python
# ❌ Bad
all_users = session.exec(select(User)).all()  # Could be millions!

# ✓ Good
users = session.exec(
    select(User).offset(skip).limit(100)
).all()
```

### String-Based Queries

```python
# ❌ Bad
result = session.execute("SELECT * FROM user WHERE email = ?", (email,))

# ✓ Good
statement = select(User).where(User.email == email)
result = session.exec(statement)
```

---

## Session Management Anti-Patterns

### Not Closing Sessions

```python
# ❌ Bad
session = Session(engine)
session.add(user)
session.commit()
# Session never closed!

# ✓ Good
with Session(engine) as session:
    session.add(user)
    session.commit()
```

### Committing Inside Loops

```python
# ❌ Bad
for user_data in users_data:
    user = User(**user_data)
    session.add(user)
    session.commit()  # Slow!

# ✓ Good
users = [User(**data) for data in users_data]
session.add_all(users)
session.commit()
```

### Ignoring Transactions

```python
# ❌ Bad
user = User(email="test@example.com")
session.add(user)
# No commit - changes lost!

# ✓ Good
session.add(user)
session.commit()
```

---

## Relationship Anti-Patterns

### Missing back_populates

```python
# ❌ Bad - One-way only
class User(SQLModel, table=True):
    posts: List["Post"] = Relationship()

class Post(SQLModel, table=True):
    user: Optional[User] = Relationship()

# ✓ Good - Bidirectional
class User(SQLModel, table=True):
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    user: Optional[User] = Relationship(back_populates="posts")
```

### Forgetting Foreign Keys

```python
# ❌ Bad
class Post(SQLModel, table=True):
    user: Optional[User] = Relationship()
    # Missing user_id foreign key!

# ✓ Good
user_id: int = Field(foreign_key="user.id")
user: Optional[User] = Relationship(back_populates="posts")
```

### Cascade Deletes Without Care

```python
# ❌ Bad - Deletes all user's posts!
class User(SQLModel, table=True):
    posts: List["Post"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

# ✓ Good - Consider soft delete or explicit handling
is_deleted: bool = Field(default=False)
```

---

## Migration Anti-Patterns

### Editing Applied Migrations

```python
# ❌ Bad
# Edit migrations/versions/abc123_create_user.py after applying

# ✓ Good
# Create new migration
alembic revision -m "Add email column to user"
```

### Skipping Rollback Testing

```python
# ❌ Bad
def downgrade():
    pass  # Not implemented!

# ✓ Good
def downgrade():
    op.drop_table('user')
```

### Auto-generating Without Review

```bash
# ❌ Bad
alembic revision --autogenerate -m "Changes"
alembic upgrade head  # Applied without review!

# ✓ Good
alembic revision --autogenerate -m "Changes"
# Review generated migration
# Test on dev database
alembic upgrade head
```

---

## Security Anti-Patterns

### Storing Plain Passwords

```python
# ❌ Bad
password: str

# ✓ Good
hashed_password: str
```

### SQL Injection Vulnerability

```python
# ❌ Bad
query = f"SELECT * FROM user WHERE email = '{email}'"
session.execute(query)

# ✓ Good
statement = select(User).where(User.email == email)
```

### Exposing Sensitive Data

```python
# ❌ Bad
class User(SQLModel, table=True):
    hashed_password: str  # Exposed in API!

# ✓ Good
class UserResponse(BaseModel):
    email: str
    # password excluded
```

---

## Performance Anti-Patterns

### Loading All Data

```python
# ❌ Bad
all_users = session.exec(select(User)).all()

# ✓ Good
users = session.exec(select(User).limit(100)).all()
```

### Missing Indexes

```python
# ❌ Bad
email: str = Field(unique=True)  # No index!

# ✓ Good
email: str = Field(unique=True, index=True)
```

### No Connection Pooling

```python
# ❌ Bad
engine = create_engine(DATABASE_URL)

# ✓ Good
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)
```
