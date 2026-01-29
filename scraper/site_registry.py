import json

class SiteRegistry:
    def __init__(self):
        with open("./scraper/HeadlineConfig.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

    
    def get_url(self,name:str) -> str:
        return self.config[name]["url"]


    def get_names(self) -> list[str]:
        return list(self.config.keys())

    def get_story_selector(self, name:str):
        return self.config[name]["select_term"]
    
    def is_in_attr(self, site_name, element_type):
        return self.config[site_name][element_type]["in_attr"]
    
    def get_element_selector(self, name:str, element_type):
        element_select_term = self.config.get(name, {}).get(element_type)
        
        return element_select_term
