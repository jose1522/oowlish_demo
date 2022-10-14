import pytest


@pytest.fixture(scope="module")
def youtube_transcript():
    """Sample raw transcript from youtube"""
    return [
        {
            "text": "Grand Potter has hit the ground running",
            "start": 0.0,
            "duration": 3.179,
        },
        {"text": "at Chelsea the big question on", "start": 1.8, "duration": 3.66},
        {
            "text": "everyone's lips is is his Chelsea better",
            "start": 3.179,
            "duration": 3.72,
        },
        {
            "text": "than Thomas tickle so on the board in",
            "start": 5.46,
            "duration": 2.94,
        },
    ]
