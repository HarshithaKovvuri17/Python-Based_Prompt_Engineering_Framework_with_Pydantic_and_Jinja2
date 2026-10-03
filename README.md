# 🧠 Python Prompt Engineering Framework with Pydantic and Jinja2

### A reusable Python framework for building, validating, rendering, and chaining LLM prompts using **Pydantic + Jinja2**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-green.svg)](https://docs.pydantic.dev/)
[![Jinja2](https://img.shields.io/badge/Jinja2-3.x-red.svg)](https://jinja.palletsprojects.com/)
[![PyYAML](https://img.shields.io/badge/PyYAML-6.x-yellow.svg)](https://pyyaml.org/)
[![Pytest](https://img.shields.io/badge/Pytest-7%2B-orange.svg)](https://pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 📌 Overview

The **Python Prompt Engineering Framework** is a modular framework designed to manage LLM prompts outside application source code.

Instead of hardcoding prompts directly inside Python using large strings or f-strings, this project stores prompts as reusable **YAML or JSON configuration files**.

The framework then:
- Validates prompt definitions using **Pydantic** schema models.
- Loads templates automatically from disk directories.
- Renders dynamic prompt content using **Jinja2**.
- Detects missing input variables before rendering with pre-flight checks.
- Provides clear custom exception handling (`MissingVariableError`, `TemplateLoadError`).
- Supports 5 core prompt-engineering patterns out of the box.
- Executes multiple prompts sequentially through **Prompt Chaining** with automatic state management.
- Runs comprehensive unit tests with **Pytest**.

The framework is intentionally independent of any specific LLM provider. It focuses on the **prompt management and execution layer**, allowing seamless integration with OpenAI, Gemini, Anthropic, local Ollama models, or custom LLM pipelines.

---

# 🎯 Problem Statement & Solution Architecture

### The Problem
In many AI applications, prompts are directly embedded inside Python source code:

```python
# Hardcoded prompt - brittle and difficult to maintain
prompt = f"""
Summarize the following text in {max_words} words:

{text}
"""
```

As an application grows, this approach creates major bottlenecks:
- **Tightly Coupled**: Prompts are scattered across codebase business logic.
- **Difficult to Maintain & Tune**: Non-technical domain experts cannot modify prompts without code deployment.
- **Runtime Crash Risk**: Missing input variables cause partial substitutions or silent bugs at runtime.
- **No Standardization**: Different developers format prompt templates inconsistently.

### The Solution
This framework decouples **prompt template definitions** into configuration files (`.yaml` / `.json`) and processes them through 4 clean architectural layers:

```text
  Prompt Templates (.yaml / .json)
                 │
                 ▼
  TemplateLoader (Registry & File Discovery)
                 │
                 ▼
  Pydantic Validation (PromptTemplate Model)
                 │
                 ▼
  RenderEngine (Jinja2 + Pre-flight Check)
                 │
                 ▼
  PromptChain (Sequential State Pipeline)
                 │
                 ▼
    LLM / AI Application Execution
```

---

# 📂 Repository Directory Structure

```text
Python-Based_Prompt_Engineering_Framework_with_Pydantic_and_Jinja2/
├── pyproject.toml              # Build & dependency configuration
├── README.md                   # Detailed framework documentation
├── testing.md                  # Verification commands & guide
├── examples.py                 # End-to-end demonstration script
├── .gitignore                  # Git untracked pattern filters
├── src/
│   └── prompt_engine/
│       ├── __init__.py         # Package entry point & version exports
│       ├── schema.py           # Pydantic schema model (PromptTemplate)
│       ├── loader.py           # YAML/JSON loader & registry (TemplateLoader)
│       ├── engine.py           # Jinja2 render engine (RenderEngine)
│       ├── chaining.py         # Sequential prompt execution (PromptChain)
│       └── exceptions.py       # Custom exception hierarchy
├── templates/                  # Production-ready prompt templates
│   ├── zero_shot_summarizer.yaml
│   ├── zero_shot_translator.json
│   ├── few_shot_sentiment.yaml
│   ├── few_shot_classifier.json
│   ├── cot_math_solver.yaml
│   ├── cot_logic_puzzle.json
│   ├── role_python_expert.yaml
│   ├── role_financial_analyst.json
│   ├── structured_json_extractor.yaml
│   └── structured_sql_generator.json
└── tests/                      # Automated unit test suite
    ├── __init__.py
    ├── test_schema.py          # Schema validation tests
    ├── test_loader.py          # Template discovery & file parsing tests
    ├── test_engine.py          # Render engine & pre-flight check tests
    └── test_chaining.py        # Sequential pipeline execution tests
```

---

# 🚀 Core Modules & Architecture

### 1. Pydantic Schema Validation (`src/prompt_engine/schema.py`)
Defines the strict schema contracts required for every prompt template:

```python
class PromptTemplate(BaseModel):
    name: str                  # Unique identifier
    description: str           # Purpose description
    input_variables: List[str] # Required input variable keys
    template: str              # Jinja2 template string
```

### 2. Template Loader (`src/prompt_engine/loader.py`)
Scans directories, reads YAML/JSON files, validates contents against `PromptTemplate`, and maintains an in-memory template registry:

```python
from prompt_engine import TemplateLoader

loader = TemplateLoader("templates")
template = loader.get("zero_shot_summarizer")
print(loader.list_templates())
```

### 3. Jinja2 Render Engine (`src/prompt_engine/engine.py`)
Renders templates with strict variable checking using Jinja2 `StrictUndefined`:

```python
from prompt_engine import RenderEngine, MissingVariableError

engine = RenderEngine()

# Raises MissingVariableError if required variable 'max_words' is omitted
rendered_text = engine.render(template, text_to_summarize="Input text...", max_words=15)
```

### 4. Prompt Chaining (`src/prompt_engine/chaining.py`)
Executes sequences of prompts, passing outputs from one step into subsequent steps as inputs:

```python
from prompt_engine import PromptChain, ChainStep

chain = PromptChain(loader=loader)
steps = [
    ChainStep(template="zero_shot_summarizer", output_key="summary_output"),
    ChainStep(template="zero_shot_translator", input_mapping={"text": "summary_output"}),
]
results = chain.execute_chain(steps, initial_inputs={"text_to_summarize": "...", "max_words": 20, "source_language": "English", "target_language": "Spanish"})
```

---

# 🌟 Supported Prompt Engineering Patterns

The framework includes pre-built templates demonstrating 5 essential prompt engineering patterns:

### 1. Zero-Shot Prompting
- **YAML (`templates/zero_shot_summarizer.yaml`)**:
  ```yaml
  name: zero_shot_summarizer
  description: Summarizes text directly without prior examples.
  input_variables:
    - text_to_summarize
    - max_words
  template: |
    Please summarize the following text concisely in no more than {{ max_words }} words.

    Text:
    {{ text_to_summarize }}

    Summary:
  ```
- **JSON (`templates/zero_shot_translator.json`)**:
  ```json
  {
    "name": "zero_shot_translator",
    "description": "Translates text directly into a target language.",
    "input_variables": ["source_language", "target_language", "text"],
    "template": "Translate the following {{ source_language }} text into {{ target_language }}.\n\nText:\n{{ text }}\n\nTranslation:\n"
  }
  ```

### 2. Few-Shot Prompting
- **YAML (`templates/few_shot_sentiment.yaml`)**:
  Dynamic iteration over example objects using Jinja2 `{% for ex in examples %}` loop construct.
- **JSON (`templates/few_shot_classifier.json`)**:
  Support ticket classification with dynamic few-shot example formatting.

### 3. Chain-of-Thought (CoT) Reasoning
- **YAML (`templates/cot_math_solver.yaml`)**:
  Prompts step-by-step reasoning using structured XML response tags `<reasoning>` and `<final_answer>`.
- **JSON (`templates/cot_logic_puzzle.json`)**:
  Guides step-by-step logical deduction for constraint-satisfaction puzzles.

### 4. Role-Based / Persona Prompting
- **YAML (`templates/role_python_expert.yaml`)**:
  Configures persona of a Senior Python Architect for technical code reviews.
- **JSON (`templates/role_financial_analyst.json`)**:
  Configures persona of a Senior Financial Analyst for quarterly revenue evaluations.

### 5. Structured Output Generation
- **YAML (`templates/structured_json_extractor.yaml`)**:
  Generates strict schema-compliant JSON outputs without markdown wrapper blocks.
- **JSON (`templates/structured_sql_generator.json`)**:
  Translates natural language questions into database-specific SQL queries based on table schemas.

---

# ⚡ Quick Start Guide

### Installation
Clone the repository and install in editable mode with development dependencies:

```bash
git clone https://github.com/HarshithaKovvuri17/Python-Based_Prompt_Engineering_Framework_with_Pydantic_and_Jinja2.git
cd Python-Based_Prompt_Engineering_Framework_with_Pydantic_and_Jinja2
pip install -e .[dev]
```

### Basic Example Usage
```python
from prompt_engine import TemplateLoader, RenderEngine

# Initialize loader and engine
loader = TemplateLoader("templates")
engine = RenderEngine()

# Get zero-shot summarizer template
template = loader.get("zero_shot_summarizer")

# Render with variables
rendered_prompt = engine.render(
    template,
    text_to_summarize="Decoupling prompt engineering from application logic enhances maintainability.",
    max_words=10,
)

print(rendered_prompt)
```

---

# 🧪 Verification & Testing Guide

### 1. Run Automated Unit Tests (Pytest)
```bash
python -m pytest -v
```

Output:
```text
============================= test session starts =============================
collected 12 items

tests/test_chaining.py ..                                                [ 16%]
tests/test_engine.py ...                                                 [ 41%]
tests/test_loader.py ....                                                [ 75%]
tests/test_schema.py ...                                                 [100%]

============================= 12 passed in 0.14s ==============================
```

### 2. Run End-to-End Demonstration Script
```bash
python examples.py
```

### 3. Quick PowerShell Verification One-Liners
- **Verify Package Version**:
  ```powershell
  python -c "import prompt_engine; print('Version:', prompt_engine.__version__)"
  ```
- **Verify Loaded Templates**:
  ```powershell
  python -c "from prompt_engine import TemplateLoader; print(TemplateLoader('templates').list_templates())"
  ```

---

# 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
