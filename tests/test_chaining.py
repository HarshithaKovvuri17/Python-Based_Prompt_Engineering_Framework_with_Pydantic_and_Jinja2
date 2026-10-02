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

    def mock_llm(prompt: str) ->