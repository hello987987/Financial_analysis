from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeout

import requests
from requests import RequestException
class HtmlFetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-AU,en;q=0.9"
        }

    def fetch(self, url: str) -> str:
        try:
            http_response = self._request_get(url)
            
            if http_response.ok:
                return http_response.text

            return self._headless_get(url)

        except (RequestException, PlaywrightTimeout):
            return ""

    def _request_get(self, url:str) -> requests.Response:
        http_response = requests.get(
            url,
            timeout=10,
            headers=self.headers)  
        return http_response

    def _headless_get(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                return page.content()
            finally:
                browser.close()
