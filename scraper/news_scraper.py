from scraper.html_fetcher import HtmlFetcher
from scraper.site_registry import SiteRegistry
from scraper.story_extractor import StoryExtractor
from scraper.story_registry import StoryRegistry
import csv

class NewsScraper:
    def __init__(self):
        self.html_fetcher = HtmlFetcher()
        self.site_registry = SiteRegistry()
        self.story_extractor = StoryExtractor(self.site_registry)
        self.story_registry = StoryRegistry()
        

    def scrape_headlines(self, pathname):
        self.file_pathname = pathname
        site_keys = self.site_registry.get_names()

        for i, site in enumerate(site_keys):
            
            site_url = self.site_registry.get_url(site)
            current_html = self.html_fetcher.fetch(site_url)
            
            self.story_extractor.extract_and_save_stories(site, current_html)

        self.Generate_Csv(self.story_extractor.get_saved_stories())

    def Generate_Csv(self, Registry):
        if not Registry:
            raise Exception("registry is not defined")

        file = self.file_pathname
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["site_origin", "title", "desc", "url"]
            )
            writer.writeheader()
            writer.writerows(Registry)

if __name__ == "__main__":
    ns = NewsScraper()
    ns.scrape_headlines("test.csv")