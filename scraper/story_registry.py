class StoryRegistry:
    def __init__(self):
        self.story_registry = []

    def append_story(self, site_origin, headline, description, url):
        self.story_registry.append({
                "headline": headline if headline else "NO_HEADLINE",
                "site_origin" : site_origin if site_origin else "UNKNON_ORIGIN",
                "desc": description if description else "NO_DESCRIPTION",
                "url": url if url else "NO_URL"
        })
    
    def get_story_registry(self):
        return self.story_registry