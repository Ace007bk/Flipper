from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

user_data = {}

@app.route('/')
def home():
    return "✅ Telegram Bot is live on Fly.io"

@app.route('/webhook', methods=["POST"])
def webhook():
    update = request.get_json()
    print("📩 Incoming Telegram update:", update)

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text == "/start":
            reply = "🚀 Welcome to the FLIP Volume Bot!\nUse /set_token <your-token> to begin."
            send_message(chat_id, reply)

        elif text.startswith("/set_token"):
            token = text.split(" ", 1)[1] if " " in text else None
            if token:
                if chat_id not in user_data:
                    user_data[chat_id] = {}
                user_data[chat_id]["token"] = token
                reply = f"✅ Target token set to:\n{token}"
            else:
                reply = "❌ Please provide a token. Example:\n/set_token H6s6CW..."
            send_message(chat_id, reply)

        else:
            reply = "❓ Unknown command. Try /start or /set_token"
            send_message(chat_id, reply)

    return "OK"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("❌ Failed to send message:", e)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
