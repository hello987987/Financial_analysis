#TODO:
#Take| A single story_registry element (REQUIRED PEICES URL, name)
#Return| The Time extracted from the true article
#Method| Use BS4 and my html grabber and find the time on the html
from scraper.html_fetcher import HtmlFetcher
from bs4 import BeautifulSoup as bs
from dateutil import parser


class TimeFixer:
    def __init__(self):
        pass

    def getTime(self, story):
        url = story["url"]
        fetcher = HtmlFetcher()
        page_html = fetcher.fetch(url)

        soup = bs(page_html, "html.parser")

        time_tag = soup.find("time", {"data-testid": "published-timestamp"})
        if time_tag and time_tag.has_attr("datetime"):
            return parser.parse(time_tag["datetime"])

        return None


if __name__ == "__main__":
    time = TimeFixer()

    reg = [
    {
        "site_origin": "nytimes.com",
        "url": "https://www.cnbc.com/2026/02/27/us-iran-nuclear-talks-oil-middle-east.html",
    }]
    for i in reg:
        cur_test = time.getTime(i)
        print(cur_test)
