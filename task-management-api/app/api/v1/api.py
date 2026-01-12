"""
API v1 router that includes all endpoint routers.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import tasks

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(tasks.router)
