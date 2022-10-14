from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Stores the settings for the worker.
    https://pydantic-docs.helpmanual.io/usage/settings/
    """
    PROJECT_NAME: str = "Media to text summarizer"
    API_V1_STR: str = "/api/v1"
    DEFAULT_PORT: int = 5000
    PROJECT_VERSION: str = "1.0.0"
    DOCS_URL: str = "/docs"


settings = Settings()
