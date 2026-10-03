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
    print("\n---