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
