from rss_feed import RSSFeed
from gemini import Gemini
from broadcast import Broadcast

def main():
    feed = RSSFeed()
    gemini = Gemini()
    broadcast = Broadcast()

    scraped_payload = """
        #     POWER ADVISORY: MANUAL LOAD DROPPING IN PARTS OF CEBECO III COVERAGE
        #     Date: June 27, 2026
        #     7:00PM - 8:00PM
        #     Ang National Grid Corporation of the Philippines (NGCP) mipatuman og Manual Load Dropping (MLD) sa isla sa Cebu, nga nakaapekto sa pipila ka mga lugar nga sakop sa CEBECO III, tungod sa kakulang sa power generation.
        #     Sa napahigayon nga MLD, makasinati og temporaryong brownout o power interruptions ang sa lungsod sa Balamban area karong adlawa.
        #     """

    #response = feed.fetch_cebeco_advisories()
    response = scraped_payload

    if not response is None:
        power_outage_feed = gemini.process_advisory_with_ai(scraped_payload)
        broadcast.broadcast_to_telegram(power_outage_feed)
        print("Message broadcasted successfully!")
    else:
        print("No Power Outage in Balamban")

if __name__ == "__main__":
    main()