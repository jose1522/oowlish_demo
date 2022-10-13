import gc
from unittest import mock

import pytest
from torch.cuda import empty_cache
from transformers import Pipeline

from models.summarization import LongTextSummarizer


@pytest.fixture(scope="module")
def summarizer():
    """Instance of LongTextSummarizer"""
    obj = LongTextSummarizer()
    yield obj
    del obj
    gc.collect()
    empty_cache()


@mock.patch.object(Pipeline, "run_single")
def test_inference(mock_pipeline: mock.MagicMock, summarizer):
    """Checks that the class processes the output of the forward call correctly.
    This is not a high fidelity inference test"""
    expected = "foo bar baz bae "*2
    mock_pipeline.return_value = {"summary_text": expected}
    actual = summarizer("At the offices of my city’s largest newspaper...")
    assert actual == expected
