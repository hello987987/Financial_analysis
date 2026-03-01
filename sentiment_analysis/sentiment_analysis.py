import csv
from transformers import pipeline
import spacy
from pathlib import Path
from CompanyResolver import CompanyResolver
import re
from datetime import datetime
#from scraper import 

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = PROJECT_ROOT / "csv_data"

class SentimentAggregator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment = pipeline( "sentiment-analysis", model="ProsusAI/finbert")
        self.company_sentiment: dict[str, list[dict[str, object]]] = {}
        self.company_resolver = CompanyResolver(
            PROJECT_ROOT / "sentiment_analysis" / "company_map.json"
        )

    def normalise_title(title) -> str:
        title = title.lower()
        title = re.sub(r"[^a-z0-9\s]", " ", title)
        title = re.sub(r"\s+", " ", title).strip()
        return title

    def analyse_title(self, title: str) -> dict[str, object]:
        title = self.normalise_title(title)
        result = self.sentiment(title)[0]
        return {
        'sentiment' : result["label"].lower(),
        'confidence' : result["score"]
        }
    
    def extract_entities(self, text: str) -> list[str]:
        doc = self.nlp(text)
        companies = set()

        for ent in doc.ents:
            if ent.label_ == "ORG":
                canon = self.company_resolver.resolve(ent.text)
                if canon:
                    companies.add(canon)

        return list(companies)
    
    def process_csv(self, csv_path: Path) -> None:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "").strip()
                if not title:
                    continue

                publisher = row.get("site_origin", "") 
                time = datetime.strptime(row.get("time", ""))
                sent = self.analyse_title(title)
                entities = self.extract_entities(title)

                article = {
                    "publisher": publisher,
                    "title": title,
                    "time" : time,
                    "sentiment": sent["sentiment"],
                    "confidence": sent["confidence"],
                    "weighted sentiment": (
                        sent["confidence"] if sent["sentiment"] == "positive"
                        else -sent["confidence"] if sent["sentiment"] == "negative"
                        else 0.0
                        )
                }

                for ent in entities:
                    self.company_sentiment.setdefault(ent, []).append(article)
                    
    def process_folder(self, folder_path: Path) -> None:
        folder = Path(folder_path)

        for csv_file in folder.glob("*.csv"):
            publisher = csv_file.stem
            self.process_csv(
                csv_path=csv_file
            )


    #testing function, ignore
    def print_summary(self, per_company = 3): 
        for company, articles in self.company_sentiment.items():
            print(f"\n{company} ({len(articles)} articles)")
            for a in articles[:per_company]:
                print(" -", a["sentiment"], f"({a['confidence']:.2f})", ":", a["title"], ":", a["publisher"],)

if __name__ == "__main__":
    agg = SentimentAggregator()
    agg.process_folder(CSV_DIR)
    agg.print_summary(per_company=3)