def test_playwright_fixture_is_ready(page):
    page.goto("https://www.example.com")
    assert "Example" in page.title()