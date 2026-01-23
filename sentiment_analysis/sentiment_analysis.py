import csv
from transformers import pipeline
import spacy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = PROJECT_ROOT / "csv_data"

class SentimentAggregator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment = pipeline( "sentiment-analysis", model="ProsusAI/finbert")
        self.company_sentiment = {}

    def analyse_title(self, title):
        result = self.sentiment(title)[0]
        return {
        'sentiment' : result["label"].lower(),
        'confidence' : result["score"]
        }
    
    def extract_entities(self, text):
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    
    def process_csv(self, csv_path):
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get("title", "").strip()
                if not title:
                    continue

                publisher = row.get("publisher", "") # Column needs to be added

                sent = self.analyse_title(title)
                entities = self.extract_entities(title)

                article = {
                    "publisher": publisher,
                    "title": title,
                    "sentiment": sent["sentiment"],
                    "confidence": sent["confidence"],
                }

                for ent in entities:
                    self.company_sentiment.setdefault(ent, []).append(article)
    # Need to store csv's in csv_data
    def process_folder(self, folder_path):
        folder = Path(folder_path)

        for csv_file in folder.glob("*.csv"):
            publisher = csv_file.stem
            self.process_csv(
                csv_path=csv_file
            )

    #testing function
    def print_summary(self, per_company = 3): 
        for company, articles in self.company_sentiment.items():
            print(f"\n{company} ({len(articles)} articles)")
            for a in articles[:per_company]:
                print(" -", a["sentiment"], f"({a['confidence']:.2f})", ":", a["title"], ":", a["publisher"],)

if __name__ == "__main__":
    agg = SentimentAggregator()
    agg.process_folder(CSV_DIR)
    agg.print_summary(per_company=3)