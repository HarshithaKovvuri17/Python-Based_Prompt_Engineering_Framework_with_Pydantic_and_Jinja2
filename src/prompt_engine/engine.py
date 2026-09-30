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

        # Pre-flight check: Verify all variables listed in template.input_variables are present
        missing_vars = template.validate_inputs(provided_vars)
        if missing_vars:
            raise MissingVariableError(
                template_name=template.name,
                missing_variables=missing_vars,
            )

        try:
            # Compile Jinja2 template string
            jinja_template = self.env.from_string(template.template)
            # Render with provided_vars
            rendered_prompt = jinja_template.render(**provided_vars)
            return rendered_prompt
        except UndefinedError as e:
            # Catch any Jinja undefined error if jinja template uses variables not listed in input_variables
            raise PromptEngineError(
                f"Jinja rendering error for template '{template.name}': {e}"
            ) from e
        except Exception as e:
            raise PromptEngineError(
                f"Unexpected rendering error for template '{template.name}': {e}"
            ) from e
