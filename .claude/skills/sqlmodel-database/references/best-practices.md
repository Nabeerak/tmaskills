# SQLModel Best Practices

## Table of Contents

- [Model Design](#model-design)
- [Session Management](#session-management)
- [Query Optimization](#query-optimization)
- [Relationships](#relationships)
- [Migrations](#migrations)
- [Testing](#testing)
- [Security](#security)
- [Performance](#performance)

---

## Model Design

### Use Type Hints

```python
# ✓ Good
email: str = Field(unique=True)
age: Optional[int] = None

# ❌ Bad
email = Field(unique=True)
age = None
```

### Set Field Constraints

```python
# ✓ Good
username: str = Field(min_length=3, max_length=50)
price: float = Field(gt=0)

# ❌ Bad
username: str
price: float
```

### Use Audit Fields

```python
created_at: datetime = Field(default_factory=datetime.utcnow)
updated_at: Optional[datetime] = None
```

---

## Session Management

### Use Context Managers

```python
# ✓ Good
with Session(engine) as session:
    session.add(user)
    session.commit()

# ❌ Bad
session = Session(engine)
session.add(user)
session.commit()
# Session never closed!
```

### Dependency Injection (FastAPI)

```python
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/users")
def get_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()
```

---

## Query Optimization

### Use Eager Loading

```python
# ✓ Good - One query
from sqlalchemy.orm import selectinload

users = session.exec(
    select(User).options(selectinload(User.posts))
).all()

# ❌ Bad - N+1 queries
users = session.exec(select(User)).all()
for user in users:
    posts = user.posts  # Separate query for each user!
```

### Select Specific Columns

```python
# ✓ Good - Only needed columns
statement = select(User.id, User.email)

# ❌ Bad - All columns
statement = select(User)
```

### Add Indexes

```python
email: str = Field(unique=True, index=True)  # ✓
user_id: int = Field(foreign_key="user.id", index=True)  # ✓
```

---

## Relationships

### Use back_populates

```python
# ✓ Good
class User(SQLModel, table=True):
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    user: Optional[User] = Relationship(back_populates="posts")

# ❌ Bad - Missing back_populates
class User(SQLModel, table=True):
    posts: List["Post"] = Relationship()
```

### Validate Foreign Keys

```python
# ✓ Good
user_id: int = Field(foreign_key="user.id")

# ❌ Bad
user_id: int  # No constraint
```

---

## Migrations

1. Review auto-generated migrations
2. Test on development database
3. Make migrations reversible
4. Keep migrations small
5. Commit migrations to version control

---

## Testing

### Use Test Database

```python
@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    SQLModel.metadata.drop_all(engine)
```

### Test with Rollback

```python
def test_create_user(session):
    user = User(email="test@example.com")
    session.add(user)
    session.commit()

    assert user.id is not None
    # Session rolled back after test
```

---

## Security

### Never Store Plain Passwords

```python
# ✓ Good
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])
hashed_password: str = pwd_context.hash("plaintext")

# ❌ Bad
password: str = "plaintext"
```

### Validate User Input

```python
# ✓ Good
from pydantic import EmailStr

email: EmailStr = Field(unique=True)

# ❌ Bad
email: str  # No validation
```

### Use Parameterized Queries

```python
# ✓ Good - SQLModel handles this
statement = select(User).where(User.email == user_email)

# ❌ Bad - SQL injection risk
query = f"SELECT * FROM user WHERE email = '{user_email}'"
```

---

## Performance

### Batch Operations

```python
# ✓ Good
session.add_all(users)
session.commit()

# ❌ Bad
for user in users:
    session.add(user)
    session.commit()  # Many commits!
```

### Use Pagination

```python
# ✓ Good
statement = select(User).offset(skip).limit(limit)

# ❌ Bad
users = session.exec(select(User)).all()  # All records!
```

### Connection Pooling

```python
# ✓ Good
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)

# ❌ Bad
engine = create_engine(DATABASE_URL)  # No pooling config
```
