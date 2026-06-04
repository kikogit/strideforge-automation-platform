from playwright.sync_api import Page

from common_utils.logging import FrameworkLogger


class BasePage:
    """
    Base class for all UI page objects.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.logger = FrameworkLogger.get_logger(self.__class__.__name__)

    def navigate_to(self, url: str) -> None:
        self.logger.info("Navigating to URL: %s", url)
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url