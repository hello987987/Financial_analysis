from playwright.sync_api import sync_playwright
import requests

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

    def fetch(self, url:str):# TODO: make this try headless if bad return code.
        http_response = self._request_get(url)
        return http_response.text

    def _request_get(self, url:str):
        http_response = requests.get(url, timeout=10)
        return http_response

    def _headless_get():
        pass