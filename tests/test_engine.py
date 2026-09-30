"""
Unit tests for RenderEngine and pre-flight input variable validation.
"""

import pytest
from prompt_engine.schema import PromptTemplate
from prompt_engine.engine import RenderEngine
from prompt_engine.exceptions import MissingVariableError, PromptEngineError


def test_render_engine_success():
    tmpl = PromptTemplate(
        name="greeting",
        description="Greets user",
        input_variables=["name", "topic"],
        template="Hello {{ name }}, let's learn {{ topic }}!",
    )
    engine = RenderEngine()
    result = engine.render(tmpl, name="Alice", topic="Python")
    assert result == "Hello Alice, let's learn Python!"


def test_render_engine_missing_variable():
    tmpl = PromptTemplate(
        name="user_profile",
        description="Displays profile",
        input