from typing import Generator
from unittest import mock

import pytest
from transformers import Pipeline


@pytest.fixture(scope="package")
def mock_nlp_inference() -> Generator:
    """Fixture that mocks the nlp inference function"""
    with mock.patch.object(Pipeline, "run_single") as m:
        m.return_value = {"summary_text": True}
        yield m
