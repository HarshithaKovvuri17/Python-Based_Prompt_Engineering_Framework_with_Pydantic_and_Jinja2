"""
Jinja2 rendering engine with strict variable validation.
"""

from typing import Any, Dict
from jinja2 import Environment, StrictUndefined, UndefinedError

from .schema import PromptTemplate
from .exceptions import MissingVariableError, PromptEngineError


class RenderEngine:
    """
    Renders Jinja2 template strings with runtime variable substitution
    and strict pre-flight input validation.
    """

    def __init__(self, undefined_behavior=StrictUndefined):
        """
        Instantiates the Jinja2 Environment with StrictUndefined to ensure
        unbound template variables trigg