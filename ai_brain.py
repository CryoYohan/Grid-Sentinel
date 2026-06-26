from google import genai
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

def process_advisory_with_ai(raw_text):
    # Dynamically fetch today's date (e.g., "June 26, 2026")
    current_date_str = datetime.now().strftime("%B %d, %Y")

    prompt = f"""
    You are the core intelligence engine for 'Grid Sentinel', a localized power outage alert system for Balamban, Cebu.

    Today's Date is: {current_date_str}

    Analyze the following raw power advisory text from CEBECO III:
    \"\"\"
    {raw_text}
    \"\"\"

    CRITICAL VALIDATION STEPS:
    1. DATE CHECK: Extract the scheduled date of the outage. If the scheduled outage date has completely passed (is older than or equal to {current_date_str}), or if the interruption window is already over, you MUST reply with exactly: SKIP_BROADCAST
    2. LOCATION CHECK: Look closely at the text. If it explicitly lists affected areas and Balamban (or its sitios/barangays) is NOT among them, you MUST reply with exactly: SKIP_BROADCAST

    If the advisory passes both checks (meaning it is a future or active outage affecting Balamban), generate a community alert broadcast matching these strict constraints:
    - Language: Conversational, urgent Cebuano (Bisaya) that locals in Balamban use naturally. Do not use stiff, textbook translations.
    - Structure: 
        * Lead with a clear headline identifying it as a CEBECO III Power Advisory.
        * Use bolding for the exact Date and Time Window.
        * Bullet point the specific affected sitios/barangays in Balamban.
        * Give a brief, friendly reminder to charge devices.
    - Do not include any introductory remarks, metadata, or explanations. Output ONLY the raw Cebuano alert text.
    """

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    return response.text.strip()


if __name__ == "__main__":
    # The exact raw text output from your feed scraper
    scraped_payload = """
    POWER ADVISORY: MANUAL LOAD DROPPING IN PARTS OF CEBECO III COVERAGE
    Date: June 25, 2026
    7:00PM - 8:00PM
    Ang National Grid Corporation of the Philippines (NGCP) mipatuman og Manual Load Dropping (MLD) sa isla sa Cebu, nga nakaapekto sa pipila ka mga lugar nga sakop sa CEBECO III, tungod sa kakulang sa power generation.
    Sa napahigayon nga MLD, makasinati og temporaryong brownout o power interruptions ang pipila ka mga lugar nga nasulod sa coverage area karong adlawa.
    """

    print("🧠 Passing payload to Gemini Brain...")
    ai_decision = process_advisory_with_ai(scraped_payload)

    print("\n--- AI OUTPUT ---")
    print(ai_decision)
    print("-----------------\n")

    if "SKIP_BROADCAST" in ai_decision:
        print("🛡️ Guard Active: Pipeline stopped. Stale or irrelevant data filtered out successfully.")
    else:
        print("🚀 Pipeline approved! Proceeding to broadcast channel.")