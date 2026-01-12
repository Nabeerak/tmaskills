"""
FastAPI application initialization and configuration.
Main entry point for the Task Management API.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.api import api_router
from app.exceptions.handlers import (
    TaskNotFoundException,
    DatabaseException,
    task_not_found_handler,
    validation_exception_handler,
    database_exception_handler,
    general_exception_handler
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup: Create database tables
    print("🚀 Starting up Task Management API...")
    await init_db()
    print("✅ Database tables created/verified")

    yield

    # Shutdown: Cleanup if needed
    print("👋 Shutting down Task Management API...")


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="""
    Task Management API with full CRUD operations.

    Features:
    - Create, read, update, and delete tasks
    - Filter tasks by status (pending, in_progress, completed)
    - Filter tasks by priority (low, medium, high)
    - Pagination support for all list endpoints
    - Automatic API documentation
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(TaskNotFoundException, task_not_found_handler)
app.add_exception_handler(DatabaseException, database_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include API routers
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint - API health check and information.
    """
    return {
        "message": "Task Management API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
