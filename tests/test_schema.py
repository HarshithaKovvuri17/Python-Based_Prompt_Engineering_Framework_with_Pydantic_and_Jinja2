"""
Unit tests for the PromptTemplate Pydantic schema.
"""

import pytest
from pydantic import ValidationError
from prompt_engine.schema import PromptTemplate


def test_valid_prompt_template():
    data = {
        "name": "test_prompt",
        "description": "A test prompt template",
        "input_variables": ["var1", "var2"],
        "template": "Hello {{ var1 }}, welcome to {{ var2 }}!",
    }
    tmpl = PromptTemplate(**data)
    assert tmpl.name == "test_prompt"
    assert tmpl.description == "A test prompt template"
    assert tmpl.input_variables == ["var1", "var2"]
    assert tmpl.template == "Hello {{ var1 }}, welcome to {{ var2 }}!"


def test_missing_required_fields():
    # Missing 'template'
    data = {
        "name": "invalid_prompt",
        "description": "Missing template field",
        "input_variables": ["var1"],
    }
    with pytest.raises(ValidationError):
        PromptTemplate(**data)


def test_validate_inputs_helper():
    tmpl = PromptTemplate(
        