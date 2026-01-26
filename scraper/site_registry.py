import json

class SiteRegistry:
    def __init__(self):
        with open("./scraper/HeadlineConfig.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

    
    def get_url(self,name:str):
        return self.config[name]["url"]


    def get_names(self):
        return list(self.config.keys())


    def get_story_selector(self, name:str):
        return self.config[name]["select_term"]