"""
Custom exception classes for the Prompt Engineering Framework.
"""

from typing import List, Union


class PromptEngineError(Exception):
    """Base exception class for all errors in the prompt engineering framework."""
    pass


class MissingVariableError(PromptEngineError):
    """
    Raised when required variables defined in the prompt template's
    'input_variables' schema are missing from the runtime render arguments.
    """

    def __init__(self, template_name: str, missing_variables: Union[str, List[str]]):
        self.template_name = template_name
        if isinstance(missing_variables, str):
            self.missing_variables = [missing_variables]
        else:
            self.missing_variables = list(missing_variables)

        vars_str = ", ".join(f"'{v}'" for v in self.missing_variables)
        if len(self.missing_variables) == 1:
            msg = f"Template '{template_name}' requires variable {vars_str} which was not provided."
        else:
            msg = f"Template '{template_name}' requires variables [{vars_str}] which were not provided."

        super().__init__(msg)


class TemplateLoadError(PromptEngineError):
    """Raised when a template file cannot be loaded or parsed."""

    def __init__(self, file_path: str, reason: str):
        self.file_path = file_path
        self.reason = reason
        super().__init__(f"Failed to load template from '{file_path}': {reason}")
