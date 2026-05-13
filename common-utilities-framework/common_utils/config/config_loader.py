"""All frameworks need configuration.
   Centralizing config loading avoids duplicate YAML-reading logic in UI/API/Mobile.
   Author: Kiran Kotian"""

from pathlib import Path
from typing import Any

import yaml

from common_utils.exceptions import ConfigurationError


class ConfigLoader:

    """
    Loads YAML configuration files for different environments.
    Responsibility:
    - Locate config files
    - Validate file existence
    - Parse YAML safely
    - Return configuration as dictionary
    - Author: Kiran Kotian

    """

    def __init__(self, config_root: str | Path = "config/environments") -> None:
        self.config_root = Path(config_root)

    def load_environment_config(self, environment: str) -> dict[str, Any]:
        if not environment:
            raise ConfigurationError("Environment name cannot be empty.")

        config_file = self.config_root / f"{environment}.yaml"

        if not config_file.exists():
            raise ConfigurationError(
                f"Configuration file not found for environment '{environment}'. "
                f"Expected path: {config_file}"
            )

        try:
            with config_file.open("r", encoding="utf-8") as file:
                config = yaml.safe_load(file)
        except yaml.YAMLError as error:
            raise ConfigurationError(
                f"Invalid YAML format in configuration file: {config_file}"
            ) from error

        if not isinstance(config, dict):
            raise ConfigurationError(
                f"Configuration file must contain a YAML dictionary: {config_file}"
            )

        return config