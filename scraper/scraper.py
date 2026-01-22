from bs4 import BeautifulSoup as bs
from pathlib import Path
from json_registry_parser import SelectorRegistry
from playwright.sync_api import sync_playwright
import requests
import csv


class scraper:

    def __init__(self):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-AU,en;q=0.9"
        }
        
        self.site_registry = SelectorRegistry()


    def Save_Scrape(self, filename: str, path: str, debug:bool = False): #TODO: Refactor nested for-loop and generalise for all sites
        self.story_registry = []
        self.csv_filename = filename
        self.path = path
        self.debug = debug
        
        
        sites = self._Get_Sites_Data()
        self.print_debug(f"found {len(sites)} in config")

        for index, site_data in enumerate(sites):
            soup = bs(site_data["html"], 'html.parser')

            stories = soup.select(self.site_registry.get_spec("yahoo"))

            self.print_debug(f"site {index} has {len(stories)} stories")

            for story in stories:
                st = story.find(attrs={"aria-label": True})
                desc = story.find("p")
                title = st["aria-label"]
                url = st["href"]
                self.story_registry.append({
                    "title": title if title else "NO_TITLE",
                    "url": url if url else "NO_URL",
                    "desc": desc.get_text(strip=True) if desc else "NO_DESC"
                })
        self.Generate_Csv(self.story_registry)

    
    def _Get_Sites_Data(self):
        site_data = []

        for index,name in enumerate(self.site_registry.get_site_names()):
            status, data = self._headless_fetch_html(self.site_registry.get_url(name))
            self.print_debug(f"site {index} : {status}")
            site_data.append({
                "html": data,
                "spec": self.site_registry.get_spec(name)
                })
            
        return site_data
    
    def _headless_fetch_html(self, url:str):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            response = page.goto(url, wait_until="networkidle")
            html = page.content()
            status = response.status if response else None
            browser.close()
            return status, html

    def Generate_Csv(self, Registry):
        if not Registry:
            raise Exception("registry is not defined")

        file = self.path + self.csv_filename
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["title", "url", "desc"]
            )
            writer.writeheader()
            writer.writerows(Registry)
    
    def print_debug(self, string: str):
        if self.debug:
            print(string)

if __name__ == "__main__":
    sc = scraper()
    sc.Save_Scrape("test.csv","", True)