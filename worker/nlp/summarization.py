from functools import lru_cache
from pathlib import Path

import torch
from transformers import pipeline


class BaseSummarizer:
    """Base class of summarization model."""

    def __init__(self, **kwargs):
        self.model = None
        self.unused = kwargs
        self.assets_folder = Path().joinpath("nlp/assets").absolute()
        self.model_name = ""

    @property
    def model_path(self):
        return str(self.assets_folder.joinpath(self.model_name))

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
        self.model_name = "long-text-summarizer"
        self.model = pipeline(
            "summarization",
            self.model_path,
            device=0 if torch.cuda.is_available() else -1,
        )

    @lru_cache(maxsize=32)
    def summarize(self, text: str, max_length: int = 300, min_length: int = 300) -> str:
        result = self.model(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return result.get("summary_text")
