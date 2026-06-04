from ui_core.browser import BrowserManager
from ui_core.pages import BasePage, ExamplePage


def test_browser_manager_can_be_created():
    browser_manager = BrowserManager()
    assert browser_manager.get_base_url() == "https://example.com"
    assert browser_manager.get_browser_name() == "chromium"
    assert browser_manager.get_default_timeout() == 30000

def test_base_page_can_be_imported():
    return BasePage is not None

def test_example_page_can_be_imported():
    return ExamplePage is not None

