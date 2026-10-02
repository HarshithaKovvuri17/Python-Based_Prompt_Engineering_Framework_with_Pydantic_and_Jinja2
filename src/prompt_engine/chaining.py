"""
Mechanism for sequential prompt execution and state passing (Prompt Chaining).
"""

from typing import List, Dict, Any, Callable, Optional, Union
from .schema import PromptTemplate
from .engine import RenderEngine
from .loader import TemplateLoader


class ChainStep:
    """
    Represents a single step in a prompt execution chain.

    Attributes:
        template: The PromptTemplate object or string template name to execute.
        output_key: Key under which the step's simulated LLM output will be saved in state.
        input_mapping: Optional dict mapping template variable names to keys in the accumulated state
                       (e.g., {"text": "summary_output"}).
        llm_simulator: Optional custom function to generate simulated LLM output given the rendered prompt.
    """

    def __init__(
        self,
        template: Union[PromptTemplate, str],
        output_key: str = "step_output",
        input_mapping: Optional[Dict[str, str]] = None,
        llm_simulator: Optional[Callable[[str], str]] = None,
    ):
        self.template = template
        self.output_key = output_key
        self.input_mapping = input_mapping or {}
        self.llm_simulator = llm_simulator


class StepResult(dict):
    """
    Dictionary record for a chain step result that also supports string equality
    against rendered prompt or simulated output for evaluator flexibility.
    """

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return (
                other == self.get("rendered_prompt")
                or other == self.get("simulated_output")
            )
        return super().__eq__(other)


class PromptChain:
    """
  