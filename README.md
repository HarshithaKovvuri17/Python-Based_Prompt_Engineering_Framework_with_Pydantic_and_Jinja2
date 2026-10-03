# 🧠 Python Prompt Engineering Framework
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
# 🎯 Problem Statement
In many AI applications, prompts are directly embedded inside Python code:
```python
prompt = f"""
Summarize the following text in {max_words} words:
{text}
"""
```
As an application grows, this approach can make prompts:
- Difficult to maintain
- Difficult to reuse
- Hard to test
- Tightly coupled with application logic
- Difficult for non-developers to modify
- More difficult to organize across multiple AI workflows
This project solves these problems by separating **prompt configuration** from **Python application logic**.
Instead, prompts are stored as structured files:
```text
templates/
├── zero_shot_summarizer.yaml
├── few_shot_sentiment.yaml
├── role_python_expert.yaml
└── structured_json_extractor.yaml
```
Python is then responsible for loading, validating, rendering, and chaining these templates.
---
# 💡 Solution
The framework introduces four major layers:
```text
Prompt Templates
      │
      ▼
Template Loader
      │
      ▼
Pydantic Validation
      │
      ▼
Jinja2 Render Engine
      │
      ▼
Rendered Prompt
      │
      ▼
Prompt Chain
      │
      ▼
LLM / Application
```
This creates a clean separation between:
```text
Prompt Configuration
        +
Prompt Validation
        +
Prompt Rendering
        +
Prompt Workflow Management
```
---
# ✨ Key Features
## 1. 📄 YAML and JSON Template Support
Prompt templates can be written using either:
- YAML
- JSON
Example:
```yaml
name: zero_shot_summarizer
description: Summarizes text directly without prior examples.
input_variables:
  - text_to_summarize
  - max_words
template: |
  Summarize the following text in no more than {{ max_words }} words.
  Text:
  {{ text_to_summarize }}
  Summary:
```
---
## 2. 🛡️ Pydantic Validation
Every prompt template is validated against a Pydantic model.
A valid template contains:
| Field | Description |
|---|---|
| `name` | Unique template identifier |
| `description` | Description of the prompt |
| `input_variables` | Variables required during rendering |
| `template` | Jinja2 prompt content |
Example:
```python
from prompt_engine import PromptTemplate
template = PromptTemplate(
    name="greeting",
    description="Creates a greeting",
    input_variables=["name"],
    template="Hello {{ name }}!"
)
```
Invalid templates are rejected during loading instead of silently causing problems later.
---
# 🔥 3. Jinja2 Dynamic Prompt Rendering
The framework uses Jinja2 to dynamically populate prompts.
Example:
```text
Hello {{ name }}!
```
Python:
```python
rendered = engine.render(
    template,
    name="Harshitha"
)
```
Output:
```text
Hello Harshitha!
```
Jinja2 also supports:
- Variables
- Loops
- Conditions
- Nested objects
- Lists
- Dictionaries
Example:
```jinja2
{% for example in examples %}
Question: {{ example.question }}
Answer: {{ example.answer }}
{% endfor %}
```
This makes the framework suitable for dynamic few-shot prompting.
---
# 🚨 4. Strict Input Validation
Before rendering a prompt, the framework checks whether all required variables are available.
For example:
```yaml
input_variables:
  - text_to_summarize
  - max_words
```
If the application provides only:
```python
engine.render(
    template,
    text_to_summarize="Sample text"
)
```
The framework raises:
```text
MissingVariableError:
Template 'zero_shot_summarizer' requires variable 'max_words'
which was not provided.
```
This prevents incomplete prompts from reaching an LLM.
---
# 🔗 5. Prompt Chaining
The framework supports sequential prompt execution.
The output of one prompt can become the input of another prompt.
Example workflow:
```text
Input Text
    │
    ▼
┌─────────────────────┐
│ Summarization Prompt│
└─────────────────────┘
    │
    ▼
Summary
    │
    ▼
┌─────────────────────┐
│ Translation Prompt  │
└─────────────────────┘
    │
    ▼
Translated Summary
```
This is implemented using:
```python
PromptChain
ChainStep
```
Example:
```python
steps = [
    ChainStep(
        template="zero_shot_summarizer",
        output_key="summary_output"
    ),
    ChainStep(
        template="zero_shot_translator",
        output_key="translated_summary",
        input_mapping={
            "text": "summary_output"
        }
    )
]
```
The framework automatically maintains the state between steps.
---
# 🧩 6. Five Prompt Engineering Patterns
The project includes **10 ready-to-use templates** covering five common prompting patterns.
### Zero-Shot Prompting
```text
zero_shot_summarizer.yaml
zero_shot_translator.json
```
### Few-Shot Prompting
```text
few_shot_sentiment.yaml
few_shot_classifier.json
```
### Chain-of-Thought Style Prompting
```text
cot_math_solver.yaml
cot_logic_puzzle.json
```
### Role-Based Prompting
```text
role_python_expert.yaml
role_financial_analyst.json
```
### Structured Output Prompting
```text
structured_json_extractor.yaml
structured_sql_generator.json
```
---
# 🏗️ System Architecture
```text
                        ┌─────────────────────────┐
                        │   YAML / JSON Templates │
                        │                         │
                        │  • Zero-Shot            │
                        │  • Few-Shot             │
                        │  • CoT                  │
                        │  • Role-Based           │
                        │  • Structured Output    │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │     TemplateLoader      │
                        │                         │
                        │ • Scan directory        │
                        │ • Read YAML / JSON      │
                        │ • Parse templates       │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │    Pydantic Schema      │
                        │                         │
                        │ • Validate structure    │
                        │ • Validate fields       │
                        │ • Validate inputs       │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │      RenderEngine       │
                        │                         │
                        │ • Jinja2 Environment    │
                        │ • StrictUndefined       │
                        │ • Variable validation   │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │    Rendered Prompt      │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │      PromptChain        │
                        │                         │
                        │ • Multiple steps        │
                        │ • State management      │
                        │ • Input mapping         │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │      LLM / AI App       │
                        └─────────────────────────┘
```
---
# 📁 Project Structure
```text
Python-Based_Prompt_Engineering_Framework_with_Pydantic_and_Jinja2/
│
├── src/
│   └── prompt_engine/
│       ├── __init__.py
│       ├── schema.py
│       ├── loader.py
│       ├── engine.py
│       ├── chaining.py
│       └── exceptions.py
│
├── templates/
│   ├── cot_logic_puzzle.json
│   ├── cot_math_solver.yaml
│   ├── few_shot_classifier.json
│   ├── few_shot_sentiment.yaml
│   ├── role_financial_analyst.json
│   ├── role_python_expert.yaml
│   ├── structured_json_extractor.yaml
│   ├── structured_sql_generator.json
│   ├── zero_shot_summarizer.yaml
│   └── zero_shot_translator.json
│
├── tests/
│   ├── __init__.py
│   ├── test_chaining.py
│   ├── test_engine.py
│   ├── test_loader.py
│   └── test_schema.py
│
├── examples.py
├── testing.md
├── pyproject.toml
└── README.md
```
---
# 🛠️ Tech Stack
| Technology | Purpose |
|---|---|
| **Python 3.9+** | Core programming language |
| **Pydantic v2** | Template schema validation |
| **Jinja2** | Dynamic prompt rendering |
| **PyYAML** | YAML template parsing |
| **JSON** | JSON template parsing |
| **Pytest** | Automated testing |
| **Setuptools** | Python package management |
---
# ⚙️ Installation
## Prerequisites
Make sure you have:
```text
Python 3.9 or higher
pip
Git
```
Check Python:
```bash
python --version
```
Expected:
```text
Python 3.9+
```
---
## 1. Clone the Repository
```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```
Move into the project:
```bash
cd Python-Based_Prompt_Engineering_Framework_with_Pydantic_and_Jinja2
```
---
## 2. Create a Virtual Environment
### Windows
```powershell
python -m venv venv
```
Activate it:
```powershell
venv\Scripts\activate
```
### Linux / macOS
```bash
python3 -m venv venv
source venv/bin/activate
```
---
## 3. Install the Project
Install the framework:
```bash
python -m pip install -e .
```
Install development dependencies:
```bash
python -m pip install -e ".[dev]"
```
The development installation includes:
```text
pytest
pytest-mock
```
---
# 🚀 Quick Start
## Step 1: Load Templates
```python
from prompt_engine import TemplateLoader
loader = TemplateLoader("templates")
print(loader.list_templates())
```
Example output:
```text
[
    'cot_logic_puzzle',
    'cot_math_solver',
    'few_shot_classifier',
    'few_shot_sentiment',
    'role_financial_analyst',
    'role_python_expert',
    'structured_json_extractor',
    'structured_sql_generator',
    'zero_shot_summarizer',
    'zero_shot_translator'
]
```
---
# 📝 Step 2: Render a Prompt
```python
from prompt_engine import TemplateLoader, RenderEngine
loader = TemplateLoader("templates")
engine = RenderEngine()
template = loader.get("zero_shot_summarizer")
result = engine.render(
    template,
    text_to_summarize="Artificial intelligence is transforming many industries.",
    max_words=10
)
print(result)
```
The Jinja2 variables are automatically replaced with the supplied values.
---
# 🔗 Step 3: Create a Prompt Chain
```python
from prompt_engine import (
    TemplateLoader,
    RenderEngine,
    PromptChain,
    ChainStep
)
loader = TemplateLoader("templates")
engine = RenderEngine()
chain = PromptChain(
    engine=engine,
    loader=loader
)
steps = [
    ChainStep(
        template="zero_shot_summarizer",
        output_key="summary_output"
    ),
    ChainStep(
        template="zero_shot_translator",
        output_key="translated_summary",
        input_mapping={
            "text": "summary_output"
        }
    )
]
initial_inputs = {
    "text_to_summarize": "Prompt engineering helps developers build reusable AI workflows.",
    "max_words": 15,
    "source_language": "English",
    "target_language": "Spanish"
}
results = chain.execute_chain(
    steps=steps,
    initial_inputs=initial_inputs
)
for result in results:
    print(result["rendered_prompt"])
```
---
# 🧪 Testing
The project includes automated unit tests covering the major framework components.
Run all tests:
```bash
python -m pytest -v
```
The tests cover:
```text
Pydantic Schema
       │
       ▼
Template Loader
       │
       ▼
Render Engine
       │
       ▼
Prompt Chaining
```
---
## Run Individual Test Files
### Schema Tests
```bash
python -m pytest tests/test_schema.py -v
```
Tests:
- Valid prompt templates
- Required fields
- Input validation
---
### Loader Tests
```bash
python -m pytest tests/test_loader.py -v
```
Tests:
- YAML loading
- JSON loading
- Invalid template handling
- Missing templates
- Directory scanning
---
### Render Engine Tests
```bash
python -m pytest tests/test_engine.py -v
```
Tests:
- Prompt rendering
- Missing variables
- Jinja2 loops
- Dynamic template processing
---
### Prompt Chain Tests
```bash
python -m pytest tests/test_chaining.py -v
```
Tests:
- Sequential execution
- State passing
- Input mapping
- Multiple chain steps
---
# ▶️ Run the Complete Demonstration
The project contains an `examples.py` file demonstrating the framework.
Run:
```bash
python examples.py
```
The demonstration covers:
```text
1. Template Loading
2. Zero-Shot Prompting
3. Few-Shot Prompting
4. Chain-of-Thought Style Prompting
5. Role-Based Prompting
6. Structured Output Prompting
7. Missing Variable Error Handling
8. Sequential Prompt Chaining
```
---
# 🔍 Example Workflow
A typical application workflow looks like this:
```text
              ┌──────────────────┐
              │ Prompt Template  │
              │ YAML / JSON      │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Template Loader  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Pydantic         │
              │ Validation       │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Jinja2 Rendering │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ Rendered Prompt  │
              └────────┬─────────┘
                       │
                       ▼
              ┌──────────────────┐
              │ LLM Application  │
              └──────────────────┘
```
For multi-step workflows:
```text
Prompt 1
   │
   ▼
Output 1
   │
   ▼
Prompt 2
   │
   ▼
Output 2
   │
   ▼
Prompt 3
   │
   ▼
Final Output
```
---
# 📚 Template Library
## Zero-Shot
### `zero_shot_summarizer.yaml`
Used for direct text summarization.
Required variables:
```text
text_to_summarize
max_words
```
### `zero_shot_translator.json`
Used for translation.
Required variables:
```text
source_language
target_language
text
```
---
## Few-Shot
### `few_shot_sentiment.yaml`
Uses examples to classify sentiment.
Required variables:
```text
examples
target_text
```
### `few_shot_classifier.json`
Uses examples to categorize customer support tickets.
Required variables:
```text
examples
ticket_description
```
---
## Chain-of-Thought Style
### `cot_math_solver.yaml`
Designed for structured mathematical problem solving.
Required variable:
```text
problem_statement
```
### `cot_logic_puzzle.json`
Designed for logical deduction problems.
Required variable:
```text
puzzle_description
```
---
## Role-Based
### `role_python_expert.yaml`
Provides a senior Python architecture/code-review role.
Required variables:
```text
primary_focus
code_snippet
```
### `role_financial_analyst.json`
Provides a financial-analysis role.
Required variables:
```text
company_name
financial_data
```
---
## Structured Output
### `structured_json_extractor.yaml`
Extracts entities into a requested JSON structure.
Required variables:
```text
unstructured_text
required_fields
```
### `structured_sql_generator.json`
Generates SQL together with structured metadata.
Required variables:
```text
database_schema
user_question
```
---
# 🧱 Core Components
## `PromptTemplate`
Responsible for defining and validating the structure of a prompt.
```python
PromptTemplate(
    name="example",
    description="Example prompt",
    input_variables=["name"],
    template="Hello {{ name }}"
)
```
---
## `TemplateLoader`
Responsible for:
- Finding template files
- Reading YAML/JSON
- Parsing template data
- Validating templates
- Registering templates
- Retrieving templates by name
Example:
```python
loader = TemplateLoader("templates")
template = loader.get("zero_shot_summarizer")
```
---
## `RenderEngine`
Responsible for:
- Jinja2 template compilation
- Input validation
- Variable substitution
- Error handling
Example:
```python
engine = RenderEngine()
result = engine.render(
    template,
    name="Harshitha"
)
```
---
## `PromptChain`
Responsible for:
- Sequential prompt execution
- State management
- Output storage
- Input mapping
- Multi-step workflows
---
## Custom Exceptions
The framework defines:
```python
PromptEngineError
MissingVariableError
TemplateLoadError
```
This provides a clear exception hierarchy for application-level error handling.
---
# 🧪 Manual Verification
The repository also contains a detailed testing guide:
```text
testing.md
```
It includes commands for:
- Package verification
- Template loading
- Prompt rendering
- Missing variable validation
- Prompt chaining
- Automated Pytest execution
Example:
```powershell
python -c "import prompt_engine; print('Package version:', prompt_engine.__version__)"
```
---
# 🔌 LLM Integration
This framework does **not require an LLM API key** for its core functionality.
It focuses on:
```text
Template Management
       +
Validation
       +
Rendering
       +
Prompt Chaining
```
The resulting prompt can then be passed to any LLM provider.
For example:
```python
rendered_prompt = engine.render(
    template,
    text_to_summarize="Your text",
    max_words=50
)
# The rendered prompt can then be passed
# to your preferred LLM client.
```
This design keeps the prompt framework independent from the model provider.
---
# 🌟 Benefits
### For Developers
- Reusable prompt components
- Cleaner Python code
- Centralized prompt management
- Easier testing
- Structured validation
### For AI Applications
- Dynamic prompts
- Few-shot examples
- Structured output instructions
- Multi-step prompt workflows
- Provider-independent prompt management
### For Teams
Prompt templates can be maintained separately from application code, making prompt updates easier to organize and review.
---
# 📊 Project Highlights
| Area | Implementation |
|---|---|
| Prompt Storage | YAML / JSON |
| Validation | Pydantic v2 |
| Rendering | Jinja2 |
| Error Handling | Custom Exceptions |
| Workflow | Prompt Chaining |
| Testing | Pytest |
| Package Structure | `src` layout |
| Configuration | `pyproject.toml` |
| LLM Provider | Provider-independent |
---
# 🤝 Contributing
Contributions are welcome.
### 1. Fork the repository
```bash
git fork <repository-url>
```
### 2. Create a feature branch
```bash
git checkout -b feature/new-feature
```
### 3. Make your changes
Add or update:
- Source code
- Tests
- Templates
- Documentation
### 4. Run tests
```bash
python -m pytest -v
```
### 5. Commit your changes
```bash
git add .
git commit -m "Add new prompt template feature"
```
### 6. Push the branch
```bash
git push origin feature/new-feature
```
### 7. Create a Pull Request
---
# 👩‍💻 Author
**Kovvuri Harshitha**
- Email: harshitahanisha@gmail.com
- GitHub: https://github.com/HarshithaKovvuri17/Python-Based_Prompt_Engineering_Framework_with_Pydantic_and_Jinja2.git
