import feedparser
import os
from dotenv import load_dotenv

load_dotenv()
RSS_FEED_URL = os.getenv("RSS_FEED")
ALERTS_FEED_URL = os.getenv("ALERTS_FEED") or RSS_FEED_URL


class RSSFeed:
    def __init__(self):
        self.feed = feedparser.parse(RSS_FEED_URL)
        self.target_municipality = "balamban"

    def fetch_cebeco_advisories(self):
        print("Initiating Grid Sentinel Scout...")
        print("Fetching CEBECO III RSS Feed...")

        self.feed = feedparser.parse(RSS_FEED_URL)

        outage_keywords = ["power interruption", "brownout", "emergency", "service interruption", "scheduled",
                           "load dropping"]

        for entry in self.feed.entries[:5]:
            text = entry.title + " " + getattr(entry, 'summary', '')
            post_url = entry.link
            text_lower = text.lower()

            # 1. Check if it's actually an outage post
            if any(keyword in text_lower for keyword in outage_keywords):

                # 2. Guard: Only proceed if it mentions Balamban OR a blanket coverage area
                if self.target_municipality in text_lower:
                    print(f"\n⚠️ [MATCH FOUND] Relevant advisory detected for Balamban region.")
                    print(f"Link: {post_url}")
                    return {"url": post_url, "text": text}
                else:
                    print(f"⏭️ Skipping post (Not relevant to Balamban).")

        print("✅ Grid is clear. No recent Balamban power interruption advisories found.")
        return None

    def fetch_yellow_red_alerts(self):
        """Return recent Yellow Alert and Red Alert entries from the alert feed."""
        print("Fetching Yellow Alert and Red Alert feed...")

        alert_feed = feedparser.parse(ALERTS_FEED_URL)
        alert_keywords = ("yellow alert", "red alert")
        alerts = []

        for entry in alert_feed.entries[:5]:
            text = entry.title + " " + getattr(entry, "summary", "")
            if any(keyword in text.lower() for keyword in alert_keywords):
                alerts.append({
                    "url": entry.link,
                    "text": text,
                })

        if alerts:
            print(f"⚠️ Found {len(alerts)} grid alert(s).")
        else:
            print("✅ No recent Yellow Alert or Red Alert entries found.")

        return alerts


if __name__ == "__main__":
    RSSFeed().fetch_cebeco_advisories()
