"""
Application configuration using Pydantic Settings.

Usage:
    from app.core.config import settings

    print(settings.PROJECT_NAME)
    print(settings.DATABASE_URL)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Environment variables can be set in .env file or system environment.
    """

    # Project Info
    PROJECT_NAME: str = "FastAPI Application"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DESCRIPTION: str = "A production-ready FastAPI application"

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"  # Default to SQLite for development

    # Security
    SECRET_KEY: str  # REQUIRED - generate with: openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    # Environment
    ENVIRONMENT: str = "development"  # development, staging, production

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra fields in .env
    )

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.ENVIRONMENT == "production"

    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins based on environment."""
        if self.ENVIRONMENT == "development":
            # Allow common development ports
            return [
                "http://localhost:3000",
                "http://localhost:8000",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:8000",
            ]
        return self.BACKEND_CORS_ORIGINS


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Settings are cached to avoid re-reading environment variables on every call.
    Clear cache with: get_settings.cache_clear()
    """
    return Settings()


# Create global settings instance
settings = get_settings()


# Example .env file:
"""
# .env

# Project
PROJECT_NAME=Task Management API
VERSION=1.0.0

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=60

# CORS (JSON array format)
BACKEND_CORS_ORIGINS=["https://myapp.com","https://www.myapp.com"]

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
"""
