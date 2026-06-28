
import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT_TOKEN var mı?:", BOT_TOKEN is not None)
print("CHAT_ID:", CHAT_ID)

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

response = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": "🎉 Tebrikler! Telegram botun çalışıyor. GitHub Actions başarılı."
    },
    timeout=20
)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)
