from bs4 import BeautifulSoup as bs
from pathlib import Path
from json_registry_parser import SelectorRegistry
from playwright.sync_api import sync_playwright
import requests
import csv


url_list = {"https://www.cnbc.com/world/?region=world",
            "https://au.finance.yahoo.com/topic/technology/",
            "https://www.reuters.com/markets/stocks/",
            }

for i,url in enumerate(url_list):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        response = page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=15000
        )

        status = response.status if response else None
        print(f"site {i} has status {status}")

        browser.close()
