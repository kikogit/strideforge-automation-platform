import pytest

from ui_core.browser import BrowserManager
from ui_core.pages import ExamplePage


@pytest.mark.ui
@pytest.mark.smoke
def test_example_page_loads_successfully(
    example_page: ExamplePage,
    browser_manager: BrowserManager,
):
    example_page.navigate_to(browser_manager.get_base_url())
    example_page.assert_page_loaded()
    assert example_page.get_heading_text() == "Example Domain"

@pytest.mark.ui
@pytest.mark.regression
def test_example_page_title(
    example_page: ExamplePage,
    browser_manager: BrowserManager,
):
    example_page.navigate_to(browser_manager.get_base_url())
    assert example_page.get_title() == "Example Domain"
