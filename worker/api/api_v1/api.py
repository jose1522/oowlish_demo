from api.api_v1.endpoints import youtube
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(youtube.router, prefix="/youtube", tags=["Model"])
