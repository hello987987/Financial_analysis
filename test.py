from scraper.news_scraper import NewsScraper as scraper

sc = scraper()
sc.scrape_headlines("csv_data/test.csv")