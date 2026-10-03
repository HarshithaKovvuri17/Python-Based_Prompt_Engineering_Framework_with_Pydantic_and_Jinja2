import sys
from pathlib import Path

# Ensure src directory is in sys.path for direct script execution
src_dir = Path(__file__).parent / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from prompt_engine import (
    TemplateLoader,
    RenderEngine,
    PromptChain,
    ChainStep,
    MissingVariableError,
)


def print_section(title: str):
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80)


def main():
    templates_dir = Path(__file__).parent / "templates"

    print_section("1. INITIALIZING TEMPLATE LOADER")
    loader = TemplateLoader(templates_dir)
    loaded_templates = loader.list_templates()
    print(f"Successfully loaded {len(loaded_templates)} templates from disk:")
    for name in loaded_templates:
        tmpl = loader.get(name)
        print(f"  - [{name}] ({tmpl.description})")

    engine = RenderEngine()

    print_section("2. DEMONSTRATING THE 5 PROMPT ENGINEERING PATTERNS")

    # Pattern 1: Zero-shot
    print("\n--- Pattern 1: Zero-shot (zero_shot_summarizer.yaml) ---")
    summarizer_tmpl = loader.get("zero_shot_summarizer")
    rendered_zero_shot = engine.render(
        summarizer_tmpl,
        text_to_summarize=(
            "Artificial intelligence frameworks require standardized design to separate template "
            "configuration from backend execution. By utilizing Pydantic for data schema validation "
            "and Jinja2 for flexible variable substitution, engineers can build robust AI pipelines."
        ),
        max_words=15,
    )
    print("Rendered Output:")
    print(rendered_zero_shot)

    # Pattern 2: Few-shot
    print("\n--- Pattern 2: Few-shot (few_shot_sentiment.yaml) ---")
    few_shot_tmpl = loader.get("few_shot_sentiment")
    examples_data = [
        {"text": "The prompt framework rendered seamlessly!", "sentiment": "Positive"},
        {"text": "The configuration file was missing required fields.", "sentiment": "Negative"},
        {"text": "The script execution finished in 2.4 seconds.", "sentiment": "Neutral"},
    ]
    rendered_few_shot = engine.render(
        few_shot_tmpl,
        examples=examples_data,
        target_text="Using Pydantic validation prevents runtime template crashes.",
    )
    print("Rendered Output:")
    print(rendered_few_shot)

    # Pattern 3: Chain-of-Thought (CoT)
    print("\n--- Pattern 3: Chain-of-Thought (cot_math_solver.yaml) ---")
    cot_tmpl = loader.get("cot_math_solver")
    rendered_cot = engine.render(
        cot_tmpl,
        problem_statement=(
            "A company processes 120 API prompt templates per minute. If they optimize their "
            "Jinja2 environment using cached template compilation, efficiency increases by 25%. "
            "How many prompt templates will they process per minute after optimization?"
        ),
    )
    print("Rendered Output:")
    print(rendered_cot)

    # Pattern 4: Role-based
    print("\n--- Pattern 4: Role-based (role_python_expert.yaml) ---")
    role_tmpl = loader.get("role_python_expert")
    code_to_review = (
        "def render_prompt(template_str, vars):\n"
        "    for k, v in vars.items():\n"
        "        template_str = template_str.replace('{{' + k + '}}', str(v))\n"
        "    return template_str"
    )
    rendered_role = engine.render(
        role_tmpl,
        primary_focus="Strict input validation, performance edge cases, and safety against partial substitution",
        code_snippet=code_to_review,
    )
    print("Rendered Output:")
    print(rendered_role)

    # Pattern 5: Structured Output
    print("\n--- Pattern 5: Structured Output (structured_json_extractor.yaml) ---")
    structured_tmpl = loader.get("structured_json_extractor")
    rendered_structured = engine.render(
        structured_tmpl,
        unstructured_text=(
            "Patient John Doe (ID: 98412) was admitted on 2026-09-25 with severe acute migraine. "
            "Attending physician: Dr. Aris Thorne."
        ),
        required_fields=["patient_name", "patient_id", "admission_date", "diagnosis", "doctor_name"],
    )
    print("Rendered Output:")
    print(rendered_structured)

    print_section("3. DEMONSTRATING STRICT VARIABLE VALIDATION (ERROR HANDLING)")
    print("Attempting to render 'zero_shot_summarizer' without providing 'max_words':")
    try:
        engine.render(
            summarizer_tmpl,
            text_to_summarize="This text is missing the max_words input argument.",
            # max_words is intentionally omitted!
        )
    except MissingVariableError as e:
        print(f"\n[SUCCESS] Custom MissingVariableError caught gracefully!")
        print(f"Error Message: {e}")

    print_section("4. DEMONSTRATING SEQUENTIAL PROMPT CHAINING")

    # We will build a 2-step chain:
    # Step 1: Summarize input text -> store output as 'step_1_summary'
    # Step 2: Role-based review or Translate summary -> use 'step_1_summary' as input text!

    chain = PromptChain(engine=engine, loader=loader)

    # Mock simulator for LLM steps
    def mock_llm_response(prompt: str) -> str:
        if "summarize" in prompt.lower():
            return "Pydantic and Jinja2 decouple prompt templates from Python code for safe, validated rendering."
        elif "translate" in prompt.lower():
            return "Pydantic y Jinja2 desacoplan las plantillas de prompts del codigo Python para un renderizado seguro y validado."
        return "Simulated LLM Response"

    chain_steps = [
        ChainStep(
            template="zero_shot_summarizer",
            output_key="summary_output",
        ),
        ChainStep(
            template="zero_shot_translator",
            output_key="translated_summary",
            input_mapping={"text": "summary_output"},
        ),
    ]

    initial_inputs = {
        "text_to_summarize": (
            "Decoupling text prompts from hardcoded Python source code is a fundamental requirement "
            "for production generative AI systems. By utilizing configuration assets in YAML/JSON and "
            "validating schemas with Pydantic, non-technical experts can safely tune prompts without code deployments."
        ),
        "max_words": 20,
        "source_language": "English",
        "target_language": "Spanish",
    }

    print("Executing 2-step prompt chain:")
    chain_results = chain.execute_chain(
        steps=chain_steps,
        initial_inputs=initial_inputs,
        default_llm_simulator=mock_llm_response,
    )

    for res in chain_results:
        print(f"\n--- Chain Step {res['step_index']}: [{res['template_name']}] ---")
        print("Rendered Prompt:")
        print(res["rendered_prompt"])
        print("\nSimulated LLM Output stored in state under key:", res["output_key"])
        print(f" -> {res['simulated_output']}")

    print("\nFinal Accumulative State across Chain:")
    for k, v in chain_results[-1]["state_after_step"].items():
        if len(str(v)) > 80:
            print(f"  - {k}: {str(v)[:77]}...")
        else:
            print(f"  - {k}: {v}")

    print_section("DEMONSTRATION COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
