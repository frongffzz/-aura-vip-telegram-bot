import os, requests
from flask import Flask, request, jsonify

BOT_TOKEN = os.environ.get("BOT_TOKEN","").strip()
BASE = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else ""
WEBSITE = "https://auravip.online"
EMOJI = "https://t.me/addemoji/Auravip11"

app = Flask(__name__)

def tg(method, payload):
    return requests.post(f"{BASE}/{method}", json=payload, timeout=15)

def set_webhook():
    url = os.environ.get("RENDER_EXTERNAL_URL","").rstrip("/")
    if BOT_TOKEN and url:
        try:
            tg("setWebhook", {"url": f"{url}/telegram", "drop_pending_updates": True})
        except Exception as e:
            print(e)

set_webhook()

@app.get("/")
def home():
    set_webhook()
    return "AURA VIP Telegram Bot is online 👑", 200

@app.get("/health")
def health():
    return jsonify(ok=True)

@app.post("/telegram")
def webhook():
    u = request.get_json(silent=True) or {}
    m = u.get("message") or {}
    text = (m.get("text") or "").strip()
    chat_id = (m.get("chat") or {}).get("id")
    if chat_id and (text == "/start" or text.startswith("/start ")):
        tg("sendMessage", {
            "chat_id": chat_id,
            "text": "👑 AURA VIP\nPremium Community & Lifestyle ✨\n\nยินดีต้อนรับสู่ AURA VIP 💗\nเลือกเมนูด้านล่างได้เลย",
            "disable_web_page_preview": True,
            "reply_markup": {
                "inline_keyboard": [
                    [{"text":"🌐 เข้าเว็บไซต์ AURA VIP","url":WEBSITE}],
                    [{"text":"💗 เพิ่ม AURA VIP Emoji","url":EMOJI}]
                ]
            }
        })
    return jsonify(ok=True)
