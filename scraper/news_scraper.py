from html_fetcher import HtmlFetcher
from site_registry import SiteRegistry
from story_extractor import StoryExtractor

class NewsScraper:
    def __init__(self):
        self.html_fetcher = HtmlFetcher()
        self.site_registry = SiteRegistry()
        self.story_extractor = StoryExtractor()

    def scrape_headlines(self,):

        site_keys = self.site_registry.get_names()

        for i, site in enumerate(site_keys):
            
            site_url = self.site_registry.get_url(site)
            current_html = self.html_fetcher.fetch(site_url)
            
            current_site_stories = self.story_extractor.breakdown_stories(site, current_html)
            #extract features and append to registry
        #generate the csv
        return current_site_stories


if __name__ == "__main__":
    ns = NewsScraper()
    print(ns.scrape_headlines())