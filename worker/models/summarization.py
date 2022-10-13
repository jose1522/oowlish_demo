from functools import lru_cache

import torch
from transformers import pipeline


class LongTextSummarizer:
    """Summarization model capable of processing long strings."""
    def __init__(self):
        self.model = pipeline(
            "summarization",
            "pszemraj/long-t5-tglobal-base-16384-book-summary",
            device=0 if torch.cuda.is_available() else -1,
        )

    @lru_cache(maxsize=32)
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
        result = self.model(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return result.get("summary_text")

    def __call__(self, *args, **kwargs) -> str:
        return self.summarize(*args, **kwargs)
