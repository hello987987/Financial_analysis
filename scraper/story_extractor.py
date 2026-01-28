from bs4 import BeautifulSoup as bs
from site_registry import SiteRegistry

class StoryExtractor:
    def __init__(self):
        self.site_registry = SiteRegistry()

    def breakdown_stories(self, name, html):
        select_string = self.site_registry.get_story_selector(name)
        print(select_string)
        
        soup = bs(html, 'html.parser')
        return soup.select(select_string)
