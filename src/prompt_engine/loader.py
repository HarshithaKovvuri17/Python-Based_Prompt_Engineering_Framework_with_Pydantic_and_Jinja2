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
            self.load_directory(direct