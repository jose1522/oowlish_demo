import gc

import pytest
from torch.cuda import empty_cache

from nlp.summarization import LongTextSummarizer


@pytest.fixture(scope="module")
def summarizer():
    """Instance of LongTextSummarizer"""
    obj = LongTextSummarizer()
    yield obj
    del obj
    gc.collect()
    empty_cache()


def test_inference(mock_nlp_inference, summarizer):
    """Checks that the class processes the output of the forward call correctly.
    This is not a high fidelity inference test"""
    actual = summarizer("At the offices of my city’s largest newspaper...")
    assert actual
