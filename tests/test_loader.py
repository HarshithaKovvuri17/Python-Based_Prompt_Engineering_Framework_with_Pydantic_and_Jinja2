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

    yaml_mo