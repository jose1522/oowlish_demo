from pydantic import BaseModel


class TextSummary(BaseModel):
    """Base class for summarized text"""

    summary: str
