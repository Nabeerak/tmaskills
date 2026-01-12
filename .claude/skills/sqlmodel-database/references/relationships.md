# SQLModel Relationships

## Table of Contents

- [Relationship Basics](#relationship-basics)
- [One-to-Many](#one-to-many)
- [Many-to-One](#many-to-one)
- [One-to-One](#one-to-one)
- [Many-to-Many](#many-to-many)
- [Self-Referential Relationships](#self-referential-relationships)
- [Cascading Operations](#cascading-operations)
- [Lazy vs Eager Loading](#lazy-vs-eager-loading)
- [Back Populates](#back-populates)

---

## Relationship Basics

Relationships connect models using `Relationship()` and foreign keys:

```python
from sqlmodel import Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")
```

**Key concepts**:
- Foreign key establishes database constraint
- Relationship enables Python object access
- `back_populates` creates bidirectional link

---

## One-to-Many

One parent has many children.

### Example: User → Posts

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)

    # One user has many posts
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")

    # Many posts belong to one user
    user: Optional[User] = Relationship(back_populates="posts")
```

### Usage

```python
# Create user with posts
user = User(email="alice@example.com")
session.add(user)
session.commit()

post1 = Post(title="First Post", content="...", user_id=user.id)
post2 = Post(title="Second Post", content="...", user_id=user.id)
session.add_all([post1, post2])
session.commit()

# Access posts through relationship
session.refresh(user)
print(f"User has {len(user.posts)} posts")
for post in user.posts:
    print(post.title)
```

---

## Many-to-One

Many children belong to one parent (inverse of one-to-many).

### Example: Comments → Post

```python
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    comments: List["Comment"] = Relationship(back_populates="post")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    post_id: int = Field(foreign_key="post.id")

    post: Optional[Post] = Relationship(back_populates="comments")
```

### Usage

```python
# Access parent from child
comment = session.get(Comment, comment_id)
print(f"Comment on: {comment.post.title}")
```

---

## One-to-One

Each record relates to exactly one other record.

### Example: User → Profile

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str

    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bio: str
    user_id: int = Field(foreign_key="user.id", unique=True)

    user: Optional[User] = Relationship(back_populates="profile")
```

**Key**: `uselist=False` makes it one-to-one, `unique=True` on foreign key enforces database constraint.

### Usage

```python
user = User(email="alice@example.com")
session.add(user)
session.commit()

profile = Profile(bio="Software developer", user_id=user.id)
session.add(profile)
session.commit()

# Access
session.refresh(user)
print(user.profile.bio)
```

---

## Many-to-Many

Records on both sides relate to multiple records on the other side.

### Example: Students ↔ Courses

Requires a **link table**:

```python
class StudentCourseLink(SQLModel, table=True):
    """Association table for many-to-many."""
    student_id: int = Field(foreign_key="student.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    courses: List["Course"] = Relationship(
        back_populates="students",
        link_model=StudentCourseLink
    )

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str

    students: List[Student] = Relationship(
        back_populates="courses",
        link_model=StudentCourseLink
    )
```

### Usage

```python
# Create students and courses
alice = Student(name="Alice")
bob = Student(name="Bob")
python_course = Course(title="Python 101")
sql_course = Course(title="SQL Fundamentals")

session.add_all([alice, bob, python_course, sql_course])
session.commit()

# Create associations
link1 = StudentCourseLink(student_id=alice.id, course_id=python_course.id)
link2 = StudentCourseLink(student_id=alice.id, course_id=sql_course.id)
link3 = StudentCourseLink(student_id=bob.id, course_id=python_course.id)

session.add_all([link1, link2, link3])
session.commit()

# Access relationships
session.refresh(alice)
print(f"Alice enrolled in: {[c.title for c in alice.courses]}")

session.refresh(python_course)
print(f"Python students: {[s.name for s in python_course.students]}")
```

### Many-to-Many with Extra Fields

```python
from datetime import datetime

class StudentCourseLink(SQLModel, table=True):
    student_id: int = Field(foreign_key="student.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)

    # Extra fields
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)
    grade: Optional[str] = None
```

---

## Self-Referential Relationships

Model relates to itself.

### Example: Employee → Manager

```python
class Employee(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    manager_id: Optional[int] = Field(default=None, foreign_key="employee.id")

    # Relationship to manager (parent)
    manager: Optional["Employee"] = Relationship(
        back_populates="subordinates",
        sa_relationship_kwargs={"remote_side": "Employee.id"}
    )

    # Relationship to subordinates (children)
    subordinates: List["Employee"] = Relationship(back_populates="manager")
```

### Usage

```python
ceo = Employee(name="CEO")
manager = Employee(name="Manager", manager_id=ceo.id)
dev1 = Employee(name="Dev 1", manager_id=manager.id)
dev2 = Employee(name="Dev 2", manager_id=manager.id)

session.add_all([ceo, manager, dev1, dev2])
session.commit()

# Access hierarchy
session.refresh(manager)
print(f"Manager: {manager.name}")
print(f"Reports to: {manager.manager.name}")
print(f"Subordinates: {[e.name for e in manager.subordinates]}")
```

---

## Cascading Operations

Control what happens to related records on delete/update.

### Cascade Delete

```python
from sqlalchemy import ForeignKey

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str

    posts: List["Post"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    )

    user: Optional[User] = Relationship(back_populates="posts")
```

**Cascade options**:
- `"all, delete-orphan"`: Delete related when parent deleted
- `"save-update"`: Update related when parent updated
- `"merge"`: Merge related when parent merged
- `"delete"`: Delete related when parent deleted

---

## Lazy vs Eager Loading

### Lazy Loading (Default)

Relationships loaded on access:

```python
user = session.get(User, user_id)
# Posts not loaded yet

posts = user.posts  # Now posts are loaded
```

### Eager Loading

Load relationships immediately:

```python
from sqlmodel import select
from sqlalchemy.orm import selectinload

# Load user with posts
statement = select(User).options(selectinload(User.posts)).where(User.id == user_id)
user = session.exec(statement).first()

# Posts already loaded, no additional query
posts = user.posts
```

**When to use**:
- Lazy: Default, load on demand
- Eager: Avoid N+1 queries, load upfront

---

## Back Populates

`back_populates` creates bidirectional relationships:

```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    posts: List["Post"] = Relationship(back_populates="user")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="posts")
```

**Benefits**:
- Navigate both directions (user.posts, post.user)
- SQLAlchemy keeps both sides in sync
- Prevents inconsistencies

**Common mistake**:
```python
# ❌ Missing back_populates - relationship one-way only
class User(SQLModel, table=True):
    posts: List["Post"] = Relationship()  # No back_populates

class Post(SQLModel, table=True):
    user: Optional[User] = Relationship()  # No back_populates
```

---

## Complete Example

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

# Many-to-Many Link Table
class ProjectMemberLink(SQLModel, table=True):
    project_id: int = Field(foreign_key="project.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    role: str = Field(default="member")
    joined_at: datetime = Field(default_factory=datetime.utcnow)

# Models with Multiple Relationships
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)

    # One-to-Many: User → Posts
    posts: List["Post"] = Relationship(back_populates="author")

    # One-to-One: User → Profile
    profile: Optional["Profile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )

    # Many-to-Many: User ↔ Projects
    projects: List["Project"] = Relationship(
        back_populates="members",
        link_model=ProjectMemberLink
    )

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author_id: int = Field(foreign_key="user.id")

    author: Optional[User] = Relationship(back_populates="posts")

    # One-to-Many: Post → Comments
    comments: List["Comment"] = Relationship(back_populates="post")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    text: str
    post_id: int = Field(foreign_key="post.id")

    post: Optional[Post] = Relationship(back_populates="comments")

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bio: str
    user_id: int = Field(foreign_key="user.id", unique=True)

    user: Optional[User] = Relationship(back_populates="profile")

class Project(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    members: List[User] = Relationship(
        back_populates="projects",
        link_model=ProjectMemberLink
    )
```

---

## Best Practices

1. **Always use back_populates** for bidirectional relationships
2. **Use link tables** for many-to-many relationships
3. **Add indexes** on foreign key columns
4. **Consider cascade behavior** carefully
5. **Use eager loading** to avoid N+1 queries
6. **Keep relationship names descriptive**
7. **Document complex relationships** with comments
8. **Test cascade deletes** before production
9. **Use Optional[] for nullable** relationships
10. **Consider relationship_kwargs** for advanced cases
