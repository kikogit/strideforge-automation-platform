import pytest

from common_utils.config import ConfigLoader, EnvironmentManager
from common_utils.exceptions import ConfigurationError


def test_config_loader_loads_local_environment():
    config = ConfigLoader().load_environment_config("local")

    assert config["environment"] == "local"
    assert "ui" in config
    assert "api" in config
    assert "mobile" in config
    assert "logging" in config
    assert "reporting" in config


def test_environment_manager_returns_local_environment_by_default():
    manager = EnvironmentManager()

    assert manager.get_environment_name() == "local"


def test_environment_manager_returns_ui_config():
    manager = EnvironmentManager("local")
    ui_config = manager.get_ui_config()

    assert ui_config["base_url"] == "https://example.com"
    assert ui_config["browser"] == "chromium"


def test_environment_manager_returns_api_config():
    manager = EnvironmentManager("local")
    api_config = manager.get_api_config()

    assert api_config["base_url"] == "https://jsonplaceholder.typicode.com"
    assert api_config["timeout"] == 30


def test_config_loader_raises_error_for_missing_environment():
    with pytest.raises(ConfigurationError):
        ConfigLoader().load_environment_config("missing_env")