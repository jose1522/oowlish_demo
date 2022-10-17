from functools import lru_cache
from pathlib import Path

import torch
from transformers import pipeline

from core.config import settings


class BaseSummarizer:
    """Base class of summarization model."""
    TASK = "summarization"
    ASSETS_FOLDER = Path().joinpath("nlp/assets").absolute()

    def __init__(self, model_name: str = None, **kwargs):
        self.model = None
        self.unused = kwargs
        self.model_name = model_name
        self._generate_model()

    @property
    def model_path(self):
        return str(self.ASSETS_FOLDER.joinpath(self.model_name))

    @property
    def device(self):
        if torch.cuda.is_available():
            return "cuda"
        elif settings.ENABLE_MPS and torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"

    def _generate_model(self) -> None:
        """Generates a model using a pipeline"""
        self.model = pipeline(
            self.TASK,
            self.model_path,
            device=self.device,
        )

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

    def __init__(self, model_name: str = "long-text-summarizer", **kwargs):
        super().__init__(model_name=model_name, **kwargs)

    @lru_cache(maxsize=32)
    def summarize(self, text: str, max_length: int = 300, min_length: int = 300) -> str:
        result = self.model(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        return result.get("summary_text")
