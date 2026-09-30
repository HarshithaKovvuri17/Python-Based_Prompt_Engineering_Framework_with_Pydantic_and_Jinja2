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
        input_variables=["username", "age"],
        template="User {{ username }} is {{ age }} years old.",
    )
    engine = RenderEngine()
    with pytest.raises(MissingVariableError) as exc_info:
        engine.render(tmpl, username="Bob")

    err = exc_info.value
    assert err.template_name == "user_profile"
    assert "age" in err.missing_variables
    assert "Template 'user_profile' requires variable 'age' which was not provided." in str(err)


def test_render_engine_jinja_loop_and_conditionals():
