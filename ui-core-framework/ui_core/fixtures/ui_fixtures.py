import pytest
from playwright.sync_api import Page

from common_utils.reporting import ReportingHelper
from ui_core.browser import BrowserManager
from ui_core.pages import ExamplePage


@pytest.fixture
def browser_manager() -> BrowserManager:
    return BrowserManager()


@pytest.fixture
def reporting_helper() -> ReportingHelper:
    return ReportingHelper()


@pytest.fixture
def configured_page(page: Page, browser_manager: BrowserManager) -> Page:
    page.set_default_timeout(browser_manager.get_default_timeout())
    return page


@pytest.fixture
def example_page(configured_page: Page) -> ExamplePage:
    return ExamplePage(configured_page)