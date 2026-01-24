import json
from pathlib import Path
from bs4 import BeautifulSoup as bs

class SelectorRegistry:
    def __init__(self):
        with open("./scraper/Config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

    def get_spec(self, site: str):
        return self.config[site]["select_term"]
    
    def get_site_names(self):
        return list(self.config.keys())
    
    def get_url(self,name:str):
        return self.config[name]["url"]
    
    def get_title(self, name:str, soup):
        if self.config[name]["title"]["in_attr"]:
            attr = self.config[name]["title"]["string"]
            st = soup.find(attrs={"aria-label": True})
            return st.get("aria-label")
        else:
            tag = self.config[name]["title"]["string"]
            title = soup.find(tag)
            return title.get_text(strip=True)
    

if __name__ == "__main__":
    s = SelectorRegistry()
    print(s.get_url_from_name("reuters"))