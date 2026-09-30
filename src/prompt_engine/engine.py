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
        unbound template variables trigger errors.
        """
        self.env = Environment(undefined=undefined_behavior)

    def render(self, template: PromptTemplate, *args: Any, **kwargs: Any) -> str:
        """
        Renders a PromptTemplate instance with runtime arguments.

        Args:
            template: Validated PromptTemplate instance.
            *args: Optional dictionary of runtime variables.
            **kwargs: Key-value pairs matching input_variables.

        Returns:
            The fully rendered prompt string.

        Raises:
            MissingVariableError: If any variable in template.input_variables is missing.
            PromptEngineError: If Jinja2 fails rendering due to undefined variables or syntax issues.
        """
        provided_vars = {}
        if args and isinstance(args[0], dict):
            provided_vars.update(args[0])
        provided_vars.update(kwargs)

        # Pre-fligh