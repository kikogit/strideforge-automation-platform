import json
from pathlib import Path
from typing import Any

import yaml

from common_utils.exceptions import TestDataError


class TestDataManager:
    """
    Centralized test data manager.

    Responsibilities:
    - Load JSON test data
    - Load YAML test data
    - Validate file existence
    - Return test data as dictionary
    - Keep test files clean and free from hard-coded data
    """

    def __init__(self, test_data_root: str | Path = "test-data") -> None:
        self.test_data_root = Path(test_data_root)

    def load_json(self, relative_file_path: str) -> dict[str, Any]:
        file_path = self.test_data_root / relative_file_path
        self._validate_file_exists(file_path)

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as error:
            raise TestDataError(f"Invalid JSON test data file: {file_path}") from error

        if not isinstance(data, dict):
            raise TestDataError(f"JSON test data must be a dictionary: {file_path}")

        return data

    def load_yaml(self, relative_file_path: str) -> dict[str, Any]:
        file_path = self.test_data_root / relative_file_path
        self._validate_file_exists(file_path)

        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file)
        except yaml.YAMLError as error:
            raise TestDataError(f"Invalid YAML test data file: {file_path}") from error

        if not isinstance(data, dict):
            raise TestDataError(f"YAML test data must be a dictionary: {file_path}")

        return data

    def get_json_record(self, relative_file_path: str, record_name: str) -> dict[str, Any]:
        data = self.load_json(relative_file_path)
        return self._get_required_record(data, relative_file_path, record_name)

    def get_yaml_record(self, relative_file_path: str, record_name: str) -> dict[str, Any]:
        data = self.load_yaml(relative_file_path)
        return self._get_required_record(data, relative_file_path, record_name)

    def _get_required_record(
        self,
        data: dict[str, Any],
        relative_file_path: str,
        record_name: str,
    ) -> dict[str, Any]:
        record = data.get(record_name)

        if not isinstance(record, dict):
            raise TestDataError(
                f"Record '{record_name}' not found or invalid in test data file: "
                f"{relative_file_path}"
            )

        return record

    @staticmethod
    def _validate_file_exists(file_path: Path) -> None:
        if not file_path.exists():
            raise TestDataError(f"Test data file not found: {file_path}")

        if not file_path.is_file():
            raise TestDataError(f"Test data path is not a file: {file_path}")