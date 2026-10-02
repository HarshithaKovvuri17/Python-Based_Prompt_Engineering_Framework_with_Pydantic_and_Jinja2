"""
Unit tests for PromptChain sequential execution and state passing.
"""

import pytest
from prompt_engine.schema import PromptTemplate
from prompt_engine.engine import RenderEngine
from prompt_engine.loader import TemplateLoader
from prompt_engine.chaining import PromptChain, ChainStep


def test_prompt_chain_execution():
    tmpl1 = PromptTemplate(
        name="step1_summary",
        description="Step 1",
        input_variables=["raw_text"],
        template="Summarize: {{ raw_text }}",
    )
    tmpl2 = PromptTemplate(
        name="step2_action",
        description="Step 2",
        input_variables=["summary"],
        template="Extract actions from summary: {{ summary }}",
    )

    engine = RenderEngine()
    chain = PromptChain(engine=engine)

    def mock_llm(prompt: str) -> str:
        if "Summarize" in prompt:
            return "Summary result"
        return "Action items result"

    steps = [
        ChainStep(template=tmpl1, output_key="summary"),
        ChainStep(template=tmpl2, output_key="action_items"),
    ]

    initial_inputs = {"raw_text": "Detailed raw text content"}
    results = chain.execute_chain(steps, initial_inputs, default_llm_simulator=mock_llm)

    assert len(results) == 2
    assert results[0]["template_name"] == "step1_summary"
    assert results[0]["simulated_output"] == "Summary result"
    assert results[1]["template_name"] == "step2_action"
    assert results[1]["rendered_prompt"] == "Extract actions from summary: Summary result"
    assert results[1]["simulated_output"] == "Action items result"
    assert results[1]["state_after_step"]["summary"] == "Summary result"
    assert results[1]["state_after_step"]["action_items"] == "Action items result"


def test_prompt_chain_with_loader_template_names(tmp_path):
    t_file = tmp_path / "t1.yaml"
    t_file.write_text(
        'name: named_t1\ndescription: Test\ninput_variables: [in_var]\ntemplate: "Prompt: {{ in_var }}"\n'
    )
    loader = TemplateLoader(tmp_path)
    chain = PromptChain(loader=loader)

    results = chain.execute_chain(
        steps=["named_t1"],
        initial_inputs={"in_var": "Hello World"},
    )
    assert len(results) == 1
    assert results[0]["template_name"] == "named_t1"
    assert results[0]["rendered_prompt"] == "Prompt: Hello World"
