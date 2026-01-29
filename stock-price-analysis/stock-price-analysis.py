import yfinance as yf
import json
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
import csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = PROJECT_ROOT / "csv_data"

class StockPriceAnalysis:
    def __init__(self, company_name):
        lookup_path = Path(__file__).parent / "company_tickers.json"
        with open(lookup_path, "r", encoding="utf-8") as f:
            self.COMPANY_TICKERS = json.load(f)
        self.company = self.COMPANY_TICKERS.get(company_name.lower())
        self.ticker = yf.Ticker(self.company)
        self.sydney_tz = ZoneInfo("Australia/Sydney")

    def read_time(self, folder_path):
        folder = Path(folder_path)


        for csv_file in folder.glob("*.csv"):
            with open(csv_file, newline = "", encoding = "utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    time_str = row.get("time_published", "").strip()
                
                article_time =  datetime.fromisoformat(time_str)
                yield csv_file.name, row, article_time


    def track_price(self, article_time):
        if article_time.tzinfo is None:
            article_time = article_time.replace(tzinfo=self.sydney_tz)
        else:
            article_time = article_time.astimezone(self.sydney_tz)


        start_time = article_time - timedelta(hours=12)
        end_time   = article_time + timedelta(hours=12)

        frame = self.ticker.history(
            start=start_time.date(),
            end=end_time.date() + timedelta(days=1),
            interval="15m")
        
        if frame.empty:
            return frame 
        frame = frame.tz_convert(self.sydney_tz)
        price_window = frame.loc[start_time:end_time]
        

        initial_open = float(price_window.iloc[0]["Open"])
        final_close = float(price_window.iloc[-1]["Close"])

        return {
            "initial_open": initial_open,
            "final_close": final_close,
            "abs_change": final_close - initial_open,
            "return_pct": (final_close / initial_open) - 1,
            "rows": len(price_window),
        }

if __name__ == "__main__":
    analysis = StockPriceAnalysis("apple")

    for file_name, row, article_time in analysis.read_articles(CSV_DIR):
        result = analysis.track_price(article_time)

        if result is None:
            print(file_name, "|", article_time, "| NO DATA")
        else:
            print(
                file_name, "|", article_time,
                "| open:", f'{result["initial_open"]:.2f}',
                "| close:", f'{result["final_close"]:.2f}',
                "| return%:", f'{result["return_pct"]*100:.2f}',
                "| rows:", result["rows"],
            )