from dotenv import load_dotenv
import os
import requests

load_dotenv()


class Broadcast:
    def __init__(self):
        self.TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")
        self.CHANNEL_ID = os.getenv("CHANNEL_ID")

    def broadcast_to_telegram(self,message):
        print("📢 Sending broadcast to Telegram Channel...")
        url = f"https://api.telegram.org/bot{self.TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": self.CHANNEL_ID, "text": message, "parse_mode": "HTML"}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Alert successfully broadcasted!")
        else:
            print(f"❌ Broadcast failed: {response.text}")


if __name__ == "__main__":
    b = Broadcast()
    b.broadcast_to_telegram("Test. Sending Message from Grid Sentinel AI Automation.")
