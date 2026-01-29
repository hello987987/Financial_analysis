from bs4 import BeautifulSoup as bs
from site_registry import SiteRegistry

class StoryExtractor:
    def __init__(self, story_registry):
        self.site_registry = story_registry
        self.site_stories = []

    def breakdown_stories(self, name, html): #GOAL: to
        select_string = self.site_registry.get_story_selector(name)
        
        soup = bs(html, 'html.parser')
        stories = soup.select(select_string)
        
        for story in stories:
            self._extract_story_features(name, story)
            
    
    def _extract_story_features(self, site_name, soup_element):
        title = self._extract_feature(site_name, soup_element, "title")
        desc =  self._extract_feature(site_name, soup_element, "desc")
        url = self._extract_feature(site_name, soup_element, "search_url")

        self.site_stories.append({
            "title": title if title else "NO_TITLE",
            "site_origin" : site_name if site_name else "UNKNON_ORIGIN",
            "desc": desc if desc else "NO_DESCRIPTION",
            "url": url if url else "NO_URL"
        })
        
    def _extract_feature(self, name:str, soup, element_type: str):
        term = self.site_registry.get_element_selector(name, element_type)
        if not term:
            return None
        term = term["string"]
        is_attribute = self.site_registry.is_in_attr(name, element_type)

        if is_attribute:
            attr = term
            st = soup.find(attrs={attr})
            return st.get(attr) if st else None
        else:
            tag = term
            tag_value = soup.find(tag)
            return tag_value.get_text(strip=True) if tag_value else None


    def get_registry(self):
        return self.site_stories