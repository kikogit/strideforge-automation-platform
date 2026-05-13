"""
Facade Pattern
Test teams should not know how YAML is loaded.They should simply ask for UI config, API config, or mobile config.
Author - Kiran Kotian
"""
import os
from typing import Any

from common_utils.config.config_loader import ConfigLoader
from common_utils.exceptions import ConfigurationError


class EnvironmentManager:
    """
    Provides access to environment-specific configuration.

    Environment resolution order:
    1. Explicit constructor value
    2. TEST_ENV environment variable
    3. Default to local
    """

    def __init__(self, environment: str | None = None) -> None:
        self.environment = environment or os.getenv("TEST_ENV", "local")
        self.config = ConfigLoader().load_environment_config(self.environment)
        self._validate_environment_name()

    def _validate_environment_name(self) -> None:
        config_env_name = self.config.get("environment")

        if config_env_name != self.environment:
            raise ConfigurationError(
                f"Environment mismatch. Requested '{self.environment}' "
                f"but config file contains '{config_env_name}'."
            )

    def get_environment_name(self) -> str:
        return self.environment

    def get_config(self) -> dict[str, Any]:
        return self.config

    def get_ui_config(self) -> dict[str, Any]:
        return self._get_required_section("ui")

    def get_api_config(self) -> dict[str, Any]:
        return self._get_required_section("api")

    def get_mobile_config(self) -> dict[str, Any]:
        return self._get_required_section("mobile")

    def get_logging_config(self) -> dict[str, Any]:
        return self._get_required_section("logging")

    def get_reporting_config(self) -> dict[str, Any]:
        return self._get_required_section("reporting")

    def _get_required_section(self, section_name: str) -> dict[str, Any]:
        section = self.config.get(section_name)

        if not isinstance(section, dict):
            raise ConfigurationError(
                f"Missing or invalid configuration section: '{section_name}'"
            )

        return section
