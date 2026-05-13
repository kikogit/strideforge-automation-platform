from datetime import datetime
from pathlib import Path

from common_utils.config import EnvironmentManager
from common_utils.exceptions import ReportingError

class ReportingHelper:
    """
    Centralized reporting and artifact path helper.

    Responsibilities:
    - Create report folders
    - Create artifact folders
    - Generate screenshot paths
    - Generate video paths
    - Generate trace paths
    - Provide Allure results directory
    - Keep artifact naming consistent across UI, API, and Mobile frameworks
    """

    def __init__(self,reports_root: str | Path = "reports") -> None:
        self.reports_root = Path(reports_root)
        self.environment_manager = EnvironmentManager()
        self.reporting_config = self.environment_manager.get_reporting_config()

    def create_reports_root(self) -> Path:
        return self._create_directory(self.reports_root)

    def get_allure_results_dir(self) -> Path:
        allure_dir = self.reporting_config.get("allure_results_dir", "allure-results")
        return self._create_directory(Path(allure_dir))

    def get_screenshots_dir(self) -> Path:
        return self._create_directory(self.reports_root / "screenshots")

    def get_videos_dir(self) -> Path:
        return self._create_directory(self.reports_root / "videos")
    
    def get_traces_dir(self) -> Path:
        return self._create_directory(self.reports_root / "traces")

    def get_html_reports_dir(self) -> Path:
        return self._create_directory(self.reports_root / "html")

    def get_junit_reports_dir(self) -> Path:
        return self._create_directory(self.reports_root / "junit")

    def build_screenshot_path(self, test_name: str, extension: str = "png") -> Path:
        file_name = self._build_artifact_file_name(test_name, extension)
        return self.get_screenshots_dir() / file_name

    def build_video_path(self, test_name: str, extension: str = "webm") -> Path:
        file_name = self._build_artifact_file_name(test_name, extension)
        return self.get_videos_dir() / file_name

    def build_trace_path(self, test_name: str, extension: str = "zip") -> Path:
        file_name = self._build_artifact_file_name(test_name, extension)
        return self.get_traces_dir() / file_name

    def build_html_report_path(self, report_name: str, extension: str = "pytest_report") -> Path:
        file_name = self._build_artifact_file_name(report_name, "html")
        return self.get_html_reports_dir() / file_name

    def build_junit_report_path(self, report_name: str = "junit_report") -> Path:
        file_name = self._build_artifact_file_name(report_name, "xml")
        return self.get_junit_reports_dir() / file_name

    def should_capture_screenshot_on_failure(self) -> bool:
        return self.reporting_config.get("screenshot_on_failure", True)
    
    def should_capture_video_on_failure(self) -> bool:
        return bool(self.reporting_config.get("video_on_failure", False))

    def _build_artifact_file_name(self, name: str, extension: str) -> str:
        clean_name = self._sanitize_name(name)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        clean_extension = extension.lstrip(".")
        return f"{clean_name}_{timestamp}.{clean_extension}"

    @staticmethod
    def _sanitize_name(name: str) -> str:
        if not name:
            raise ReportingError("Name for artifact cannot be empty.")
        allowed_chars = []

        for char in name:
            if char.isalnum() or char in ['-', '_', ' ']:
                allowed_chars.append(char)
            else:
                allowed_chars.append('_')
        return "".join(allowed_chars).strip("-")
    
    @staticmethod
    def  _create_directory(directory_path : Path) -> Path:
        try:
            directory_path.mkdir(parents=True, exist_ok=True)   
        except Exception as e:
            raise ReportingError(f"Failed to create directory at {directory_path}: {str(e)}") 
        return directory_path







