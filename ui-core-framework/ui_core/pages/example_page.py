from playwright.sync_api import expect

from ui_core.pages.base_page import BasePage


class ExamplePage(BasePage):
    """
    Page Object for https://example.com.

    This page is used only for initial framework validation.
    """

    HEADING = "h1"
    MORE_INFORMATION_LINK = "a"

    def assert_page_loaded(self) -> None:
        expect(self.page.locator(self.HEADING)).to_have_text("Example Domain")

    def get_heading_text(self) -> str:
        return self.page.locator(self.HEADING).inner_text()

    def click_more_information(self) -> None:
        self.page.locator(self.MORE_INFORMATION_LINK).click()