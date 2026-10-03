# Testing Commands

## 1. Automated Unit Tests (Pytest)

### Run All Unit Tests
```powershell
python -m pytest -v
```

### Run Specific Test Files
```powershell
# Test Pydantic Schema Validation
python -m pytest tests/test_schema.py -v

# Test Template Loader (YAML & JSON Loading)
python -m pytest tests/test_loader.py -v

# Test Jinja2 Render Engine & Variable Check
python -m pytest tests/test_engine.py -v

# Test Sequential Prompt Chaining
python -m pytest tests/test_chaining.py -v
```

### Run Specific Test Function
```powershell
python -m pytest tests/test_engine.py -k "test_render_engine_missing_variable" -v
```

---

## 2. End-to-End Demonstration Script

```powershell
python examples.py
```

---

## 3. PowerShell One-Liner Manual Verification Commands

### Verify Package Installation & Version
```powershell
python -c "import prompt_engine; print('Package version:', prompt_engine.__version__)"
```

### Verify Template Loader (Lists 10 Templates)
```powershell
python -c "from prompt_engine import TemplateLoader; print('Loaded:', TemplateLoader('templates').list_templates())"
```

### Verify Zero-Shot Template Rendering
```powershell
python -c "from prompt_engine import TemplateLoader, RenderEngine; l=TemplateLoader('templates'); e=RenderEngine(); print(e.render(l.get('zero_shot_summarizer'), text_to_summarize='Framework test', max_words=5))"
```

### Verify MissingVariableError Exception Handling
```powershell
python -c "from prompt_engine import TemplateLoader, RenderEngine; e=RenderEngine(); e.render(TemplateLoader('templates').get('zero_shot_summarizer'), text_to_summarize='Test')"
```

### Verify Sequential Prompt Chaining
```powershell
python -c "from prompt_engine import PromptChain, TemplateLoader; c=PromptChain(loader=TemplateLoader('templates')); print(c.execute_chain(['zero_shot_summarizer'], {'text_to_summarize': 'Prompt engineering test', 'max_words': 5}))"
```
