import requests
from playwright.sync_api import sync_playwright

class SiteResponseChecker:
    def __init__(self):
        self.headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )}
        

    def test_site(self, url):
        self.url = url
        self.fetch_with_requests()
        self.fetch_with_playwright()

    def fetch_with_requests(self):
        print("\n========== REQUESTS ==========")

        try:
            resp = requests.get(
                url = self.url,
                allow_redirects=True,
                timeout=10,
                headers = self.headers
            )

            print("Status:", resp.status_code)
            print("Final URL:", resp.url)
            print("HTML length:", len(resp.text))
            print("\n----- HTML START -----\n")
            print(resp.text[:1000])
            print("\n----- HTML END -----\n")

        except Exception as e:
            print("Requests error:", e)


    def fetch_with_playwright(self):
        print("\n========== PLAYWRIGHT ==========")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            try:
                response = page.goto(url, wait_until="domcontentloaded", timeout=10000)

                html = page.content()

                if response:
                    print("Status:", response.status)
                    print("Final URL:", response.url)
                else:
                    print("Status: None (no response object)")

                print("HTML length:", len(html))
                print("\n----- HTML START -----\n")
                print(html[:1000])
                print("\n----- HTML END -----\n")

            except Exception as e:
                print("Playwright error:", e)

            finally:
                browser.close()

if __name__ == "__main__":
    url = "https://www.news.com.au/technology"
    src = SiteResponseChecker()
    src.test_site(url)
