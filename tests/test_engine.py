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
        input