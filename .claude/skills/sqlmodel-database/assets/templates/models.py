"""
SQLModel database models with relationships.

This template demonstrates:
- Basic model definition with constraints
- One-to-many relationships
- Many-to-many relationships
- Audit fields (created_at, updated_at)
- Proper type hints and validation
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime


# Many-to-many link table
class UserGroupLink(SQLModel, table=True):
    """Link table for User-Group many-to-many relationship."""

    user_id: int = Field(foreign_key="user.id", primary_key=True)
    group_id: int = Field(foreign_key="group.id", primary_key=True)


class User(SQLModel, table=True):
    """User model with validation and relationships."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic fields with constraints
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address"
    )
    username: str = Field(
        unique=True,
        index=True,
        min_length=3,
        max_length=100,
        description="Unique username"
    )
    full_name: str = Field(max_length=255)

    # Boolean flags
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationships
    posts: List["Post"] = Relationship(back_populates="user")
    profile: Optional["UserProfile"] = Relationship(back_populates="user")
    groups: List["Group"] = Relationship(
        back_populates="users",
        link_model=UserGroupLink
    )


class UserProfile(SQLModel, table=True):
    """One-to-one profile for User."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key (one-to-one)
    user_id: int = Field(foreign_key="user.id", unique=True)

    # Profile fields
    bio: Optional[str] = Field(default=None, max_length=1000)
    avatar_url: Optional[str] = Field(default=None, max_length=500)
    website: Optional[str] = Field(default=None, max_length=500)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)

    # Relationship
    user: Optional[User] = Relationship(back_populates="profile")


class Post(SQLModel, table=True):
    """Post model with foreign key to User."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key
    user_id: int = Field(foreign_key="user.id", index=True)

    # Content fields
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    slug: str = Field(unique=True, index=True, max_length=250)

    # Status fields
    is_published: bool = Field(default=False)
    views: int = Field(default=0, ge=0)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    published_at: Optional[datetime] = Field(default=None)

    # Relationships
    user: Optional[User] = Relationship(back_populates="posts")
    tags: List["Tag"] = Relationship(back_populates="posts", link_model="PostTagLink")


class PostTagLink(SQLModel, table=True):
    """Link table for Post-Tag many-to-many relationship."""

    post_id: int = Field(foreign_key="post.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)


class Tag(SQLModel, table=True):
    """Tag model for categorizing posts."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Fields
    name: str = Field(unique=True, index=True, max_length=50)
    slug: str = Field(unique=True, index=True, max_length=60)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    posts: List[Post] = Relationship(back_populates="tags", link_model=PostTagLink)


class Group(SQLModel, table=True):
    """Group model for user organization."""

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Fields
    name: str = Field(unique=True, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)

    # Audit fields
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship
    users: List[User] = Relationship(
        back_populates="groups",
        link_model=UserGroupLink
    )
