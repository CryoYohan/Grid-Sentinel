from datetime import datetime
import feedparser
import os
from dotenv import load_dotenv

load_dotenv()

RSS_FEED_URL = os.getenv("RSS_FEED")


def fetch_cebeco_advisories():
    print("Initiating Grid Sentinel Scout...")
    print("Fetching CEBECO III RSS Feed...")

    feed = feedparser.parse(RSS_FEED_URL)

    outage_keywords = ["power interruption", "brownout", "emergency", "service interruption", "scheduled",
                       "load dropping"]
    target_municipality = "balamban"

    for entry in feed.entries[:5]:
        text = entry.title + " " + getattr(entry, 'summary', '')
        post_url = entry.link
        text_lower = text.lower()

        # 1. Check if it's actually an outage post
        if any(keyword in text_lower for keyword in outage_keywords):

            # 2. Guard: Only proceed if it mentions Balamban OR a blanket coverage area
            if target_municipality in text_lower:
                print(f"\n⚠️ [MATCH FOUND] Relevant advisory detected for Balamban region.")
                print(f"Link: {post_url}")
                return {"url": post_url, "text": text}
            else:
                print(f"⏭️ Skipping post (Not relevant to Balamban).")

    print("✅ Grid is clear. No recent Balamban power interruption advisories found.")
    return None


if __name__ == "__main__":
    latest_alert = fetch_cebeco_advisories()
    print(latest_alert)