from functools import lru_cache
from pathlib import Path

import torch
from transformers import pipeline

from core.config import settings


class BaseSummarizer:
    """Base class of summarization model."""

    TASK = "summarization"
    ASSETS_FOLDER = Path(__file__).parent.joinpath("assets")

    def __init__(self, model_name: str = None, **kwargs):
        self.model = None
        self.unused = kwargs
        self.model_name = model_name
        self._generate_model()

    @property
    def model_path(self):
        """Returns the path where the assets are"""
        return str(self.ASSETS_FOLDER.joinpath(self.model_name))

    @property
    def device(self):
        """Returns the appropriate device to use in the pipeline"""
        if torch.cuda.is_available():
            return "cuda"
        elif settings.ENABLE_MPS and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def _generate_model(self) -> None:
        """Generates a model using a pipeline"""
        self.model = pipeline(
            self.TASK,
            self.model_path,
            device=self.device,
        )

    def summarize(self, text: str, max_length: int = 300, min_length: int = 30) -> str:
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
    def summarize(self, text: str, max_length: int = 300, min_length: int = 30) -> str:
        result = self.model(
            text, max_length=max_length, min_length=min_length, do_sample=False
        )
        if isinstance(result, list):
            result = result[0]
        return result.get("summary_text")
