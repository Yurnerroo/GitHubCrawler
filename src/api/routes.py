from fastapi import APIRouter

from .endpoints import crawler_endpoints

api_router = APIRouter()


api_router.include_router(crawler_endpoints.router, prefix="/crawler", tags=["crawler"])
