import uvicorn
from fastapi import FastAPI

from api.api_v1.api import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=settings.PROJECT_VERSION,
    docs_url=settings.DOCS_URL,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("worker.main:app", port=settings.DEFAULT_PORT, log_level="info")
