import os
import requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""

WEBSITE = "https://auravip.online"
EMOJI = "https://t.me/addemoji/Auravip11"

app = Flask(__name__)

def tg(method, payload=None):
    if not BOT_TOKEN:
        return None
    return requests.post(f"{BASE}/{method}", json=payload or {}, timeout=20)

def send_welcome(chat_id):
    return tg("sendMessage", {
        "chat_id": chat_id,
        "text": "👑 AURA VIP\nPremium Community & Lifestyle ✨\n\nยินดีต้อนรับสู่ AURA VIP 💗\nเลือกเมนูด้านล่างได้เลย",
        "disable_web_page_preview": True,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🌐 เข้าเว็บไซต์ AURA VIP", "url": WEBSITE}],
                [{"text": "💗 เพิ่ม AURA VIP Emoji", "url": EMOJI}]
            ]
        }
    })

@app.get("/")
def home():
    return "AURA VIP Telegram Bot is online 👑", 200

@app.get("/setup")
def setup():
    if not BOT_TOKEN:
        return "BOT_TOKEN is missing", 500

    # Uses the exact public Render URL the browser is currently visiting.
    public_base = request.url_root.rstrip("/")
    webhook_url = f"{public_base}/telegram"

    r = tg("setWebhook", {
        "url": webhook_url,
        "drop_pending_updates": True
    })

    if r is None:
        return "Could not contact Telegram", 500

    return f"Webhook setup result: {r.text}\nWebhook URL: {webhook_url}", 200, {"Content-Type": "text/plain; charset=utf-8"}

@app.get("/webhook-info")
def webhook_info():
    r = tg("getWebhookInfo")
    if r is None:
        return "Could not contact Telegram", 500
    return r.text, 200, {"Content-Type": "application/json; charset=utf-8"}

@app.post("/telegram")
def webhook():
    update = request.get_json(silent=True) or {}
    message = update.get("message") or {}
    text = (message.get("text") or "").strip()
    chat_id = (message.get("chat") or {}).get("id")

    if chat_id and (text == "/start" or text.startswith("/start ")):
        send_welcome(chat_id)

    return jsonify(ok=True)

@app.get("/health")
def health():
    return jsonify(ok=True)
