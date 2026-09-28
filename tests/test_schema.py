"""
Unit tests for the PromptTemplate Pydantic schema.
"""

import pytest
from pydantic import ValidationError
from prompt_engine.schema import PromptTemplate


def test_valid_prompt_template():
    d