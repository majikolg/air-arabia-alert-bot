import os
import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://www.airarabia.com/en/offers"

def send_message(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=10
    )

try:
    response = requests.get(URL, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()

    keywords = ["sale", "offer", "discount", "deal"]

    if any(word in text for word in keywords):
        send_message("✈️ Air Arabia kampanya sayfasında yeni fırsatlar olabilir:\nhttps://www.airarabia.com/en/offers")

except Exception as e:
    send_message(f"Hata oluştu: {e}")
