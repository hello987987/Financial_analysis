from scraper.landing_scraper import LandingScraper as scraper

sc = scraper()
sc.Save_Scrape("test.csv","csv_data/", True)