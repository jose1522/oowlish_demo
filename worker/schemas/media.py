from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


class OnlineSource(BaseModel):
    """Base class for media sources"""

    url: AnyHttpUrl
    max_length: Optional[int] = 130
    min_length: Optional[int] = 30
