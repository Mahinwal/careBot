from fastapi import APIRouter
from app.api.v1.routes import healthcheck

api_router = APIRouter()
api_router.include_router(healthcheck.router)
