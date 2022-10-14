from abc import ABC
from typing import Any


class BaseMedia2Text(ABC):
    """Base class for all media to 2 extractors"""
    def __init__(self, source: str):
        self.source = source

    def _digest_source(self) -> Any:
        """
        Processes the path and returns an object that can be useful to `.extract_text`
        """
        return self.source

    def extract_text(self) -> str:
        """
        Extracts the text from the media located at the path provided.
        Returns:
            str
        """

    def __call__(self):
        """
        Shortcut for `.extract_text`
        """
        self.extract_text()
