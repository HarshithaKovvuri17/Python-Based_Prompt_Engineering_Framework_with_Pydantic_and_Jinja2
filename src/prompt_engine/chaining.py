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
    Executes a sequence of prompt templates, carrying state forward from step to step.
    """

    def __init__(
        self,
        engine: Optional[RenderEngine] = None,
        loader: Optional[TemplateLoader] = None,
    ):
        self.engine = engine or RenderEngine()
        self.loader = loader

    def _resolve_template(self, template_ref: Union[PromptTemplate, str]) -> PromptTemplate:
        if isinstance(template_ref, PromptTemplate):
            return template_ref
        elif isinstance(template_ref, str):
            if not self.loader:
                raise ValueError(
                    f"Cannot resolve template name '{template_ref}' because no TemplateLoader was provided to PromptChain."
                )
            return self.loader.get(template_ref)
        else:
            raise TypeError(f"Invalid template reference type: {type(template_ref)}")

    def execute_chain(
        self,
        steps: Optional[List[Union[PromptTemplate, str, ChainStep, Dict[str, Any]]]] = None,
        initial_inputs: Optional[Dict[str, Any]] = None,
        default_llm_simulator: Optional[Callable[[str], str]] = None,
        templates: Optional[List[Union[PromptTemplate, str, ChainStep, Dict[str, Any]]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executes an ordered chain of prompt templates sequentially.

        For each step:
        1. Prepares step inputs from accumulated state (applying input_mapping if specified).
        2. Renders the template using the inputs.
        3. Generates simulated LLM output for the prompt.
        4. Merges the output into accumulated state under output_key.

        Args:
            steps: List of templates, template names, ChainStep objects, or dict configs.
            initial_inputs: Initial state variables provided for rendering.
            default_llm_simulator: Default function to simulate LLM responses.
            templates: Alias for `steps`.

        Returns:
            List of step records detailing rendered prompts, simulated outputs, and updated states.
        """
        chain_steps = steps if steps is not None else templates
        if chain_steps is None:
            chain_steps = []
        if initial_inputs is None:
            initial_inputs = {}

        state = dict(initial_inputs)
        results = []

        for i, step_item in enumerate(chain_steps, start=1):
            input_mapping = {}
            if isinstance(step_item, ChainStep):
                template_ref = step_item.template
                output_key = step_item.output_key
                input_mapping = step_item.input_mapping
                step_simulator = step_item.llm_simulator or default_llm_simulator
            elif isinstance(step_item, dict):
                template_ref = step_item["template"]
                output_key = step_item.get("output_key", f"step_{i}_output")
                input_mapping = step_item.get("input_mapping", {})
                step_simulator = step_item.get("llm_simulator", default_llm_simulator)
            else:
                template_ref = step_item
                output_key = f"step_{i}_output"
                step_simulator = default_llm_simulator

            template = self._resolve_template(template_ref)

            # Build inputs for this step from accumulated state
            step_inputs = dict(state)
            if input_mapping:
                for target_var, state_key in input_mapping.items():
                    if state_key in state:
                        step_inputs[target_var] = state[state_key]

            # Render template with mapped step inputs
            rendered_prompt = self.engine.render(template, **step_inputs)

            # Generate simulated LLM response
            if step_simulator:
                simulated_output = step_simulator(rendered_prompt)
            else:
                simulated_output = f"[Simulated LLM Output for Step {i} ({template.name})]"

            # Store result output under output_key and common fallback keys
            state[output_key] = simulated_output
            state[f"step_{i}_output"] = simulated_output
            state["previous_output"] = simulated_output
            state["last_output"] = simulated_output

            step_record = StepResult({
                "step_index": i,
                "template_name": template.name,
                "rendered_prompt": rendered_prompt,
                "output_key": output_key,
                "simulated_output": simulated_output,
                "state_after_step": dict(state),
            })
            results.append(step_record)

        return results
