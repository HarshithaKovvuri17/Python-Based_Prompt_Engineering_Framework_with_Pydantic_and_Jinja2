"""
Pydantic schema definitions for prompt templates.
"""

from typing import List
from pydantic import BaseModel, Field, ConfigDict


class PromptTemplate(BaseModel):
    """
    Pydantic schema for validating prompt template definitions.

    Attributes:
        name: A unique identifier for the template.
        description: A human-readable explanation of what the prompt does.
        input_variables: A list of variable names required at render time.
        template: The Jinja2 formatted prompt template string.
    """

    model_config = ConfigDict(extra="ignore")

    name: str = Field(
        ...,
        description="Unique identifier for the prompt template",
        min_length=1,
    )
    description: str = Field(
        ...,
        description="Human-readable explanation of what the prompt does",
    )
    input_variables: List[str] = Field(
        default_factory=list,
        description="Definitive list of variables required at render time",
    )
    template: str = Field(
        ...,
        description="The actual prompt template string using Jinja2 syntax",
    )

    def validate_inputs(self, provided_vars: dict) -> List[str]:
        """
        Check if all required input variables are present in provided_vars.
        Returns a list of missing variable names.
        """
        provided_keys = set(provided_vars.keys())
        missing = [var for var in self.input_variables if var not in provided_keys]
        return missing
