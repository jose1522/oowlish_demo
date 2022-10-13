from abc import ABC
from typing import Any, Optional
from urllib.parse import parse_qs
from urllib.parse import urlparse

from pydantic import AnyHttpUrl
from youtube_transcript_api import YouTubeTranscriptApi


class BaseMedia2Text(ABC):
    def __init__(self, path: str):
        self.path = path

    def _digest_path(self) -> Any:
        """
        Processes the path and returns an object that can be useful to `.extract_text`
        """
        return self.path

    def extract_text(self) -> str:
        """
        Extracts the text from the media located at the path provided.
        Returns:
            str
        """
        pass

    def __call__(self):
        """
        Shortcut for `.extract_text`
        """
        self.extract_text()


class Youtube2Text(BaseMedia2Text):
    pattern = r"v=(.+)&?"
    id_param = "v"
    target_languages = ["en"]

    def __init__(self, path: AnyHttpUrl):
        super(Youtube2Text, self).__init__(path=path)

    def _digest_path(self) -> Optional[str]:
        # Extract query param "v" from url and return None if not present
        parsed_url = urlparse(self.path)
        captured_value = parse_qs(parsed_url.query).get(self.id_param, [None])[0]
        return captured_value

    def extract_text(self) -> str:
        video_id = self._digest_path()
        # Get the video transcript from Youtube
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=self.target_languages
        )  # type: List[dict]
        # Extract the text from the object and concatenate it
        return " ".join([x["text"] for x in transcript])
