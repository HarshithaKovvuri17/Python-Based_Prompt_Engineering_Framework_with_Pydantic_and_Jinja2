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
    tmpl = PromptTemplate(
        name="few_shot_test",
        description="Loops over examples",
        input_variables=["examples", "query"],
        template=(
            "{% for ex in examples %}"
            "Q: {{ ex.q }} -> A: {{ ex.a }}\n"
            "{% endfor %}"
            "Q: {{ query }} -> A:"
        ),
    )
    engine = RenderEngine()
    examples = [{"q": "1+1", "a": "2"}, {"q": "2+2", "a": "4"}]
    rendered = engine.render(tmpl, examples=examples, query="3+3")
    assert "Q: 1+1 -> A: 2" in rendered
    assert "Q: 3+3 -> A:" in rendered
