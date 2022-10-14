from typing import Optional

from pydantic import BaseModel, AnyHttpUrl


class OnlineSource(BaseModel):
    """Base class for media sources"""

    url: AnyHttpUrl
    maximum_length: Optional[int] = 130
    minimum_length: Optional[int] = 30
