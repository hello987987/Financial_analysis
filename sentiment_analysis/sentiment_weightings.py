from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
import math
import re
from difflib import SequenceMatcher

class SentimentWeightings():
    def __init__(self):
        sydney_tz = ZoneInfo("Australia/Sydney")
        sydney_time = datetime.now(sydney_tz)

    def similarity(str1, str2) -> float:
        return SequenceMatcher(None, str1, str2)
    
    def exp_decay_weight(self, article_time, tau_hours) -> float: # add timezone sepecific decay only when markets are open.
        age = self.sydney_time - article_time 
        age_hours = age.total_seconds()/3600
        return math.exp(-age_hours/tau_hours)

    def weight_news_features(self, company_sentiments, tau_hours = 3, redundancy_decay = 0.9, time_window = 6):
        def get_window(articles, t, hours):
            start = t - timedelta(hours= hours)
            return [a for a in articles if start <= a["time"] <= t]

        for company in company_sentiments:
            company_sentiments[company].sort("time")

        for company, articles in company_sentiments.items():
            # sort chronologically so "earliest gets 0.9^0"
            articles.sort(key=lambda a: a["time"])

            clusters = []  # each: {"rep": str, "count": int}

            for a in articles:
                title = a.get("title_norm") or a["title"]  # prefer normalized title if you have it

                best_idx = -1
                best_score = 0.0

                # find best matching cluster rep
                for i, c in enumerate(clusters):
                    s = self.similarity(title, c["rep"])
                    if s > best_score:
                        best_score = s
                        best_idx = i

                if best_score >= 0.6:
                    c = clusters[best_idx]
                    a["redundancy_weight"] = redundancy_decay ** c["count"]
                    c["count"] += 1
                else:
                    # new cluster resets
                    a["redundancy_weight"] = 1.0
                    clusters.append({"rep": title, "count": 1})



        
        for company, articles in company_sentiments.items():
            for article in articles:
                t = article["time"]

                window = get_window(articles, t, time_window)

                weighted_sum = 0.0
                total_weight = 0.0

                for past_article in window:
                    age = (t - past_article["time"]).total_seconds() / 3600
                    w = self.exp_decay_weight(age, tau_hours)

                    weighted_sum += w * past_article["weighted sentiment"]
                    total_weight += w

                article["news_sentiment_decayed"] = (
                    weighted_sum / total_weight if total_weight > 0 else 0.0
                )

        

        
    