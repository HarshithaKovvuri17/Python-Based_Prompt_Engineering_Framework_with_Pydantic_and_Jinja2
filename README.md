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

- Validates prompt definitions using **Pydantic**
- Loads templates automatically from a directory
- Renders dynamic content using **Jinja2**
- Detects missing input variables before rendering
- Provides clear custom exceptions
- Supports reusable prompt-engineering patterns
- Allows multiple prompts to be executed sequentially through **Prompt Chaining**
- Maintains state between chain steps
- Can be tested independently using **Pytest**

The framework is intentionally independent of any specific LLM provider. It focuses on the **prompt management and execution layer**, allowing it to be integrated with OpenAI, Gemini, Anthropic, local models, or other LLM APIs later.

---

## 🚀 Quick Start

```python
from prompt_engine import TemplateLoader, RenderEngine, PromptChain

# 1. Initialize Loader & Render Engine
loader = TemplateLoader("templates")
engine = RenderEngine()

# 2. Load & Render Zero-Shot Prompt Template
template = loader.get("zero_shot_summarizer")
rendered = engine.render(
    template,
    text_to_summarize="Decoupling prompts from code enables safe, robust generative AI pipelines.",
    max_words=10,
)
print(rendered)
```
