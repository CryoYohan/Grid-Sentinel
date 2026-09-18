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
        broadcast.broadcast_to_telegram(power_outage_feed)
        print("Message broadcasted successfully!")
    else:
        print("No Power Outage in Balamban")

    for alert in feed.fetch_yellow_red_alerts():
        alert_message = gemini.process_alert_with_ai(alert["text"])
        if alert_message != "SKIP_BROADCAST":
            broadcast.broadcast_to_telegram(alert_message)
            print("Grid alert broadcasted successfully!")

if __name__ == "__main__":
    main()
