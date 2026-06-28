import hashlib
import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

OFFERS_URL = "https://www.airarabia.com/en/offers"
STATE_FILE = Path("last_seen.json")

KEYWORDS = [
    "bangkok", "thailand", "sale", "offer", "discount", "deal",
    "super seat", "promo", "promotion", "campaign", "kampanya",
]


def send_message(text: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError("BOT_TOKEN veya CHAT_ID eksik. GitHub Secrets bölümünü kontrol edin.")

    response = requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": text, "disable_web_page_preview": False},
        timeout=20,
    )
    print("TELEGRAM_STATUS:", response.status_code)
    print("TELEGRAM_RESPONSE:", response.text)
    response.raise_for_status()


def fetch_offers_text() -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 AirArabiaAlertBot/1.0",
        "Accept-Language": "en-US,en;q=0.9,tr;q=0.8",
    }
    response = requests.get(OFFERS_URL, headers=headers, timeout=30)
    print("OFFERS_STATUS:", response.status_code)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(" ", strip=True)
    text = re.sub(r"\s+", " ", text)
    return text


def make_digest(text: str) -> str:
    normalized = text.lower().encode("utf-8", errors="ignore")
    return hashlib.sha256(normalized).hexdigest()


def load_last_digest() -> str | None:
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8")).get("digest")
    except Exception:
        return None


def save_digest(digest: str) -> None:
    STATE_FILE.write_text(json.dumps({"digest": digest}, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    text = fetch_offers_text()
    digest = make_digest(text)
    last_digest = load_last_digest()

    found_keywords = [k for k in KEYWORDS if k in text.lower()]

    print("FOUND_KEYWORDS:", ", ".join(found_keywords) if found_keywords else "none")
    print("CURRENT_DIGEST:", digest)
    print("LAST_DIGEST:", last_digest)

    if last_digest is None:
        save_digest(digest)
        send_message(
            "✅ Air Arabia bot kuruldu ve çalışıyor.\n"
            "İlk kontrol tamamlandı. Bundan sonra kampanya sayfasında değişiklik olursa haber vereceğim.\n\n"
            f"Sayfa: {OFFERS_URL}"
        )
        return

    if digest != last_digest:
        save_digest(digest)
        preview = text[:700]
        send_message(
            "✈️ Air Arabia kampanya sayfasında değişiklik tespit edildi.\n\n"
            f"Bulunan kelimeler: {', '.join(found_keywords) if found_keywords else 'özel anahtar kelime yok'}\n\n"
            f"Kontrol et: {OFFERS_URL}\n\n"
            f"Ön izleme:\n{preview}..."
        )
        return

    print("NO_CHANGE: Kampanya sayfasında yeni değişiklik yok.")


if __name__ == "__main__":
    main()
