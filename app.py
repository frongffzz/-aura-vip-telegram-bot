import os
import json
import requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
BASE = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__)


def tg(method, payload=None):
    if not BOT_TOKEN:
        return None

    return requests.post(
        f"{BASE}/{method}",
        json=payload or {},
        timeout=30
    )


def send_welcome(chat_id):
    keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "🌐 เข้าเว็บไซต์ AURA VIP",
                    "url": "https://auravip.online"
                }
            ],
            [
                {
                    "text": "💎 เข้ากลุ่มแรร์ VIP",
                    "url": "https://t.me/tded7yubb"
                }
            ],
            [
                {
                    "text": "💖 รวมงาน N•VIP คัดแล้ว",
                    "url": "https://auravip.online/vip"
                }
            ]
        ]
    }

    caption = (
        "👑 AURA VIP\n"
        "Premium Community & Lifestyle ✨\n\n"
        "ยินดีต้อนรับสู่ AURA VIP 💗\n"
        "เลือกเมนูด้านล่างได้เลย"
    )

    video_path = os.path.join(
        os.path.dirname(__file__),
        "aura_welcome.mp4.mov"
    )

    with open(video_path, "rb") as video:
        return requests.post(
            f"{BASE}/sendVideo",
            data={
                "chat_id": str(chat_id),
                "caption": caption,
                "reply_markup": json.dumps(
                    keyboard,
                    ensure_ascii=False
                )
            },
            files={
                "video": (
                    "aura_welcome.mp4",
                    video,
                    "video/mp4"
                )
            },
            timeout=60
        )


@app.get("/")
def home():
    return "AURA VIP Telegram Bot is online 👑", 200


@app.get("/setup")
def setup():
    if not BOT_TOKEN:
        return "BOT_TOKEN is missing", 500

    public_base = request.url_root.rstrip("/")
    webhook_url = f"{public_base}/telegram"

    r = tg(
        "setWebhook",
        {
            "url": webhook_url,
            "drop_pending_updates": True
        }
    )

    return (
        f"Webhook setup result:<br>{r.text}<br><br>"
        f"Webhook URL: {webhook_url}"
    )


@app.post("/telegram")
def telegram_webhook():
    update = request.get_json(silent=True) or {}

    message = update.get("message") or {}
    chat = message.get("chat") or {}
    chat_id = chat.get("id")

    text = message.get("text", "")

    if chat_id and text.startswith("/start"):
        send_welcome(chat_id)

    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)
