from fastapi import APIRouter

from api.api_v1.endpoints import youtube

api_router = APIRouter()
api_router.include_router(youtube.router, prefix="/youtube", tags=["Model"])
