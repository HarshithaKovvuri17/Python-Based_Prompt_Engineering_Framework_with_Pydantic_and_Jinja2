"""
Template loader for reading and validating YAML and JSON prompt templates from disk.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Union, Optional, List
import yaml
from pydantic import ValidationError

from .schema import PromptTemplate
from .exceptions import TemplateLoadError

logger = logging.getLogger(__name__)


class TemplateLoader:
    """
    Scans directories, reads YAML and JSON files, and validates them
    against the PromptTemplate Pydantic schema.
    """

    def __init__(self, directory: Optional[Union[str, Path]] = None):
        self.registry: Dict[str, PromptTemplate] = {}
        if directory:
            self.load_directory(directory)

    def load_file(self, file_path: Union[str, Path]) -> PromptTemplate:
        """
        Loads and validates a single template file (.yaml, .yml, or .json).
        """
        path = Path(file_path)
        if not path.is_file():
            raise TemplateLoadError(str(path), "File does not exist.")

        ext = path.suffix.lower()
        if ext not in (".yaml", ".yml", ".json"):
            raise TemplateLoadError(str(path), f"Unsupported file extension '{ext}'.")

        try:
            with open(path, "r", encoding="utf-8") as f:
                if ext in (".yaml", ".yml"):
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
        except (yaml.YAMLError, json.JSONDecodeError, OSError) as e:
            raise TemplateLoadError(str(path), f"Syntax parsing error: {e}")

        if not isinstance(data, dict):
            raise TemplateLoadError(str(path), "Template file content must be a JSON/YAML object/dictionary.")

        try:
            template_model = PromptTemplate(**data)
        except ValidationError as e:
            raise TemplateLoadError(str(path), f"Schema validation error: {e}")

        return template_model

    def load_directory(self, directory_path: Union[str, Path]) -> Dict[str, PromptTemplate]:
        """
        Scans a directory for all .yaml, .yml, and .json files, validates each,
        and adds valid templates to the registry. Logs warnings for invalid files
        without crashing the loader.
        """
        dir_path = Path(directory_path)
        if not dir_path.is_dir():
            logger.warning(f"Directory path '{directory_path}' does not exist or is not a directory.")
            return self.registry

        for path in sorted(dir_path.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in (".yaml", ".yml", ".json"):
                continue

            try:
                template = self.load_file(path)
                if template.name in self.registry:
                    logger.warning(
                        f"Overwriting existing template '{template.name}' with file '{path}'"
                    )
                self.registry[template.name] = template
            except Templat