from typing import Any

from common_utils.config import EnvironmentManager
from common_utils.logging import FrameworkLogger


class BrowserManager:
    """
    Browser configuration helper for Playwright-based UI tests.

    Responsibilities:
    - Read UI configuration from environment YAML
    - Provide browser name
    - Provide headless mode
    - Provide default timeout
    - Provide base UI URL
    """

    def __init__(self) -> None:
        environment_manager = EnvironmentManager()
        self.ui_config = environment_manager.get_ui_config()
        self.logger = FrameworkLogger.get_logger("browser_manager")

    def get_base_url(self) -> str:
        return self.ui_config["base_url"]

    def get_browser_name(self) -> str:
        return self.ui_config.get("browser", "chromium")

    def is_headless(self) -> bool:
        return bool(self.ui_config.get("headless", True))

    def get_default_timeout(self) -> int:
        return int(self.ui_config.get("default_timeout", 30000))

    def get_launch_options(self) -> dict[str, Any]:
        launch_options = {
            "headless": self.is_headless(),
        }

        self.logger.info(
            "Browser launch options resolved. Browser=%s Headless=%s",
            self.get_browser_name(),
            self.is_headless(),
        )

        return launch_options