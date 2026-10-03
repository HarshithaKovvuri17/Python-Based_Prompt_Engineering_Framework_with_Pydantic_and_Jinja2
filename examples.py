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
  