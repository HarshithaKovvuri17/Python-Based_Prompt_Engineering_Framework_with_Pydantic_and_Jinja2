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
    'input_variables' schema are missing f