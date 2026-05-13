import logging
from pathlib import Path

from common_utils.config import EnvironmentManager
from common_utils.exceptions import ConfigurationError


class FrameworkLogger:
    """
    Centralized framework logger.

    Responsibilities:
    - Read logging configuration from environment YAML
    - Create console logger
    - Create optional file logger
    - Avoid duplicate handlers
    - Provide reusable named loggers
    """

    _configured_loggers: dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(cls, name: str = "strideforge") -> logging.Logger:
        if name in cls._configured_loggers:
            return cls._configured_loggers[name]

        environment_manager = EnvironmentManager()
        logging_config = environment_manager.get_logging_config()

        log_level_name = logging_config.get("level", "INFO")
        log_to_file = logging_config.get("log_to_file", False)
        log_file_path = logging_config.get("log_file_path", "logs/automation.log")

        log_level = cls._resolve_log_level(log_level_name)

        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.propagate = False

        if not logger.handlers:
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )

            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

            if log_to_file:
                file_path = Path(log_file_path)
                file_path.parent.mkdir(parents=True, exist_ok=True)

                file_handler = logging.FileHandler(file_path, encoding="utf-8")
                file_handler.setLevel(log_level)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

        cls._configured_loggers[name] = logger
        return logger

    @staticmethod
    def _resolve_log_level(level_name: str) -> int:
        level = getattr(logging, level_name.upper(), None)

        if not isinstance(level, int):
            raise ConfigurationError(f"Invalid logging level configured: {level_name}")

        return level