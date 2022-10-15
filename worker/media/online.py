from typing import Optional, List
from urllib.parse import urlparse, parse_qs

from pydantic import AnyHttpUrl
from youtube_transcript_api import YouTubeTranscriptApi

from worker.media.base import BaseMedia2Text


class Youtube2Text(BaseMedia2Text):
    """Extracts transcripts from youtube videos"""

    pattern = r"v=(.+)&?"
    id_param = "v"
    target_languages = ["en"]

    def __init__(self, source: AnyHttpUrl):
        super().__init__(source=source)

    def _digest_source(self) -> Optional[str]:
        # Extract query param "v" from url and return None if not present
        parsed_url = urlparse(self.source)
        captured_value = parse_qs(parsed_url.query).get(self.id_param, [None])[0]
        return captured_value

    def extract_text(self) -> str:
        """Digests the source and extracts a transcript of the media
        as a string."""
        video_id = self._digest_source()
        # Get the video transcript from Youtube
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=self.target_languages
        )  # type: List[dict]
        # Extract the text from the object and concatenate it
        return " ".join([x["text"] for x in transcript])
