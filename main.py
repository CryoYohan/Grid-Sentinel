from rss_feed import RSSFeed
from gemini import Gemini
from broadcast import Broadcast

def main():
    feed = RSSFeed()
    gemini = Gemini()
    broadcast = Broadcast()

    response = feed.fetch_cebeco_advisories()

    if not response is None:
        power_outage_feed = gemini.process_advisory_with_ai(response["text"])
        print(power_outage_feed)
    else:
        print("No Power Outage in Balamban")

if __name__ == "__main__":
    main()