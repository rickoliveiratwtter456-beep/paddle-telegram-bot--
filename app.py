import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# =========================
# CONFIG
# =========================
BOT_TOKEN = "7767214512:AAHVGTipD03AgwRH2qRnNHg2vV0Gite3uT0"
VIDEO_PUBLIC_URL = "https://streamable.com/d0i9ih"

WEBHOOK_PATH = f"/{BOT_TOKEN}"

# =========================
# BOT + FLASK
# =========================
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
app = Flask(__name__)

# =========================
# /start
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text="Access exclusive content now",
            url=VIDEO_PUBLIC_URL
        )
    )

    bot.send_message(
        message.chat.id,
        "🔥 <b>Exclusive Video Content</b>\n\n"
        "Click below to watch the exclusive video:",
        reply_markup=keyboard
    )

# =========================
# TELEGRAM WEBHOOK
# =========================
@app.route(WEBHOOK_PATH, methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(
        request.data.decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

# =========================
# HEALTHCHECK
# =========================
@app.route("/", methods=["GET"])
def index():
    return "Bot is running", 200

# =========================
# START APP (SEM GUNICORN)
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        debug=False
    )
