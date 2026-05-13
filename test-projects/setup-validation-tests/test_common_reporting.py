from pathlib import Path

import pytest

from common_utils.exceptions import ReportingError
from common_utils.reporting import ReportingHelper


def test_reporting_helper_creates_reports_root():
    helper = ReportingHelper()

    reports_root = helper.create_reports_root()

    assert reports_root.exists()
    assert reports_root.is_dir()


def test_reporting_helper_creates_allure_results_dir():
    helper = ReportingHelper()

    allure_dir = helper.get_allure_results_dir()

    assert allure_dir.exists()
    assert allure_dir.is_dir()
    assert allure_dir == Path("allure-results")


def test_reporting_helper_creates_artifact_directories():
    helper = ReportingHelper()

    screenshots_dir = helper.get_screenshots_dir()
    videos_dir = helper.get_videos_dir()
    traces_dir = helper.get_traces_dir()

    assert screenshots_dir.exists()
    assert videos_dir.exists()
    assert traces_dir.exists()


def test_reporting_helper_builds_screenshot_path():
    helper = ReportingHelper()

    screenshot_path = helper.build_screenshot_path("test_login_flow")

    assert screenshot_path.parent == Path("reports/screenshots")
    assert screenshot_path.suffix == ".png"
    assert "test_login_flow" in screenshot_path.name


def test_reporting_helper_builds_video_path():
    helper = ReportingHelper()

    video_path = helper.build_video_path("test_payment_flow")

    assert video_path.parent == Path("reports/videos")
    assert video_path.suffix == ".webm"
    assert "test_payment_flow" in video_path.name


def test_reporting_helper_builds_trace_path():
    helper = ReportingHelper()

    trace_path = helper.build_trace_path("test_checkout_flow")

    assert trace_path.parent == Path("reports/traces")
    assert trace_path.suffix == ".zip"
    assert "test_checkout_flow" in trace_path.name


def test_reporting_helper_builds_html_report_path():
    helper = ReportingHelper()

    html_report_path = helper.build_html_report_path("smoke_report")

    assert html_report_path.parent == Path("reports/html")
    assert html_report_path.suffix == ".html"
    assert "smoke_report" in html_report_path.name


def test_reporting_helper_builds_junit_report_path():
    helper = ReportingHelper()

    junit_report_path = helper.build_junit_report_path("regression_report")

    assert junit_report_path.parent == Path("reports/junit")
    assert junit_report_path.suffix == ".xml"
    assert "regression_report" in junit_report_path.name


def test_reporting_helper_reads_screenshot_failure_flag():
    helper = ReportingHelper()

    assert helper.should_capture_screenshot_on_failure() is True


def test_reporting_helper_reads_video_failure_flag():
    helper = ReportingHelper()

    assert helper.should_capture_video_on_failure() is False


def test_reporting_helper_raises_error_for_empty_artifact_name():
    helper = ReportingHelper()

    with pytest.raises(ReportingError):
        helper.build_screenshot_path("")