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
        input_va