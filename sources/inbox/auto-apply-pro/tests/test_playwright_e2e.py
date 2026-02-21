from pathlib import Path
from playwright.sync_api import sync_playwright

def test_fill_mock_form():
    mock_file = Path("mock_site/form.html").resolve().as_uri()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(mock_file)
        page.fill("input[name='firstName']", "Brian")
        page.fill("input[name='lastName']", "Hannigan")
        page.fill("input[type='email']", "b@example.com")
        page.fill("input[type='tel']", "123456789")
        assert page.title() == "Mock Job Form"
        browser.close()
