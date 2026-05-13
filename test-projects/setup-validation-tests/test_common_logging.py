import logging
from pathlib import Path

from common_utils.logging import FrameworkLogger

def test_framework_logger_is_created():
    logger = FrameworkLogger.get_logger("test_logger_creation")
    assert logger is not None
    assert logger.name == "test_logger_creation"


def test_framework_logger_has_handlers():
    logger = FrameworkLogger.get_logger("test_logger_handler")
    assert len(logger.handlers) > 1

def test_framework_logger_level_is_info_by_default():
    logger = FrameworkLogger.get_logger("test_logger_level")
    assert logger.level == logging.INFO


def test_framework_logger_writes_to_log_file():
    logger = FrameworkLogger.get_logger("test_logger_file")
    logger.info("Testing framework logger file output")
    log_file = Path("logs/automation.log")
    assert log_file.exists()
    
    



