import hashlib
from unittest import mock

import pytest

from worker.media.online import Youtube2Text


class TestYoutube:
    """Tests Youtube2Text logic"""

    @pytest.fixture(
        scope="class",
        params=[
            "https://www.youtube.com/watch?v=-JAFb2bYJSs",
            "https://youtube.com/watch?v=-JAFb2bYJSs&feature=share&si=EMSIkaIECMiOmarE6JChQQ&t=5",
        ],
        ids=["single param", "many params"],
    )
    def extractor(self, request):
        """Instance of Youtube2Text"""
        return Youtube2Text(request.param)

    def test_digest_path(self, extractor):
        """Checks that the class is able to extract the video id correctly"""
        expected = "-JAFb2bYJSs"
        actual = extractor._digest_source()  # pylint: disable=protected-access
        assert actual == expected

    @mock.patch("media.media.YouTubeTranscriptApi")
    def test_extract_text(
        self, mock_youtube_api: mock.MagicMock, youtube_transcript, extractor
    ):
        """Checks that the class is able to generate the text correctly"""
        mock_get_transcript = mock.MagicMock()
        mock_get_transcript.return_value = youtube_transcript
        mock_youtube_api.get_transcript = mock_get_transcript
        text = extractor.extract_text()
        assert isinstance(text, str)
        actual = hashlib.md5(text.encode()).hexdigest()
        expected = "2a2ac3e6908f4ce0c363330cc59620a3"
        assert actual == expected
