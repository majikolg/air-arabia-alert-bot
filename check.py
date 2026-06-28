
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": "🎉 Test: Air Arabia botu çalışıyor."
    },
    timeout=10
)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)
