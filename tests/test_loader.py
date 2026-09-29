"""
Unit tests for TemplateLoader (YAML & JSON parsing, directory scanning, error tolerance).
"""

import pytest
from pathlib import Path
from prompt_engine.loader import TemplateLoader, load_templates
from prompt_engine.exceptions import TemplateLoadError


def test_load_yaml_and_json_files(tmp_path: Path):
    yaml_file = tmp_path / "valid_yaml.yaml"
    yaml_file.write_text(
        "name: yaml_tmpl\n"
        "description: YAML Description\n"
        "input_variables:\n"
        "  - user\n"
        "template: 'Hello {{ user }}'\n",
        encoding="utf-8",
    )

    json_file = tmp_path / "valid_json.json"
    json_file.write_text(
        '{\n'
        '  "name": "json_tmpl",\n'
        '  "description": "JSON Description",\n'
        '  "input_variables": ["city"],\n'
        '  "template": "Welcome to {{ city }}"\n'
        '}',
        encoding="utf-8",
    )

    loader = TemplateLoader(tmp_path)
    assert "yaml_tmpl" in loader
    assert "json_tmpl" in loader

    yaml_model = loader.get("yaml_tmpl")
    assert yaml_model.input_variables == ["user"]

    json_model = loader.get("json_tmpl")
    assert json_model.input_variables == ["city"]


def test_invalid_syntax_file_skipped(tmp_path: Path):
    valid_file = tmp_path / "good.yaml"
    valid_file.write_text(
        "name: good_tmpl\ndescription: Good\ninput_variables: []\ntemplate: Hi\n"
    )

    corrupt_yaml = tmp_path / "bad.yaml"
    corrupt_yaml.write_text("name: bad_tmpl\n  invalid: [syntax: : :\n")

    invalid_schema = tmp_path / "bad_schema.json"
    invalid_schema.write_text('{"description": "Missing name and template"}')

    loader = TemplateLoader(tmp_path)
    # Loader should log warnings for bad files and successfully load good_tmpl without crashing
    assert "good_tmpl" in loader
    assert "bad_tmpl" not in loader
    assert len(loader.list_templates()) == 1


def test_get_nonexistent_template_raises_keyerror(tmp_path: Path):
    loader = TemplateLoader(tmp_path)
    with pytest.raises(KeyError) as exc_info:
        loader.get("non_existent")
    assert "not found in loader registry" in str(exc_info.value)


def test_load_templates_helper_function(tmp_path: Path):
    f = tmp_path / "test.yaml"
    f.write_text("name: helper_test\ndescription: d\ninput_variables: []\ntemplate: t\n")
    registry = load_templates(tmp_path)
    assert "helper_test" in registry
