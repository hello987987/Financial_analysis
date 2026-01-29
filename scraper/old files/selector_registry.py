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
    
    def get_url(self,site_name:str):
        return self.config[site_name]["url"]
    
    def in_attr(self, site_name, element_type):
        return self.config[site_name][element_type]["in_attr"]
    
    def get_reg_element(self, name:str, soup, element_type: str):
        site_element_reg = self.config.get(name, {}).get(element_type)

        if site_element_reg is None:
            return None
        
        item = self.get_element(site_element_reg, soup)

        return item


    def get_element(self, element_reg , soup):

        if element_reg["in_attr"]:
            attr = element_reg["string"]
            st = soup.find(attrs={attr: True})
            return st.get(attr) if st else None
        else:
            tag = element_reg["string"]
            tag_value = soup.find(tag)
            return tag_value.get_text(strip=True) if tag_value else None
