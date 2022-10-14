from functools import lru_cache

import torch
from transformers import pipeline


class BaseSummarizer:
    """Base class of summarization model."""
    def __init__(self, **kwargs):
        self.model = None
        self.unused = kwargs

    def summarize(self, text: str, max_length: int = 300, min_length: int = 300) -> str:
        """
        Summarizes a string of any length.
        Args:
            text: string to summarize.
            max_length: maximum length of the output summary.
            min_length: minimum length of the output summary.
        Returns:
            str
        """

    def __call__(self, *args, **kwargs) -> str:
        """Shortcut for .summarize"""
        return self.summarize(*args, **kwargs)


class LongTextSummarizer(BaseSummarizer):
    """Summarization model capable of processing long strings."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = pipeline(
            "summarization",
            "pszemraj/long-t5-tglobal-base-16384-book-summary",
            device=0 if torch.cuda.is_available() else -1,
        )

    @lru_cache(maxsize=32)
    def summarize(self, text: str, max_length: int = 300, min_length: int = 300) -> str:
        result = self.model(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return result.get("summary_text")


