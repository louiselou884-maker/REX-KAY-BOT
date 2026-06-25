import telebot
from flask import Flask, jsonify, request
from threading import Thread
import random
import string
import datetime

TOKEN = "8979255574:AAH4NTObyYFLBmyYhZhS27D-huG_JFlBxn8"
ADMIN_ID = 6129372969

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

keys_db = {}

def generate_key():
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(16))

@bot.message_handler(commands=["start", "help"])
def start(message):
    text = """
🔐 REX BOT APP
الأوامر:

/key عدد_المفاتيح عدد_الأيام

مثال:
/key 3 7
"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["key"])
def create_keys(message):

    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ للمطور فقط")
        return

    try:
        _, amount, days = message.text.split()

        amount = int(amount)
        days = int(days)

    except:
        bot.reply_to(message, "مثال:\n/key 3 7")
        return

    expire_date = datetime.datetime.utcnow() + datetime.timedelta(days=days)

    generated = []

    for _ in range(amount):
        key = generate_key()

        keys_db[key] = {
            "days": days,
            "expires": expire_date.strftime("%d-%m-%Y %H:%M:%S"),
            "used": False
        }

        generated.append(key)

    msg = f"""✅ {amount} Keys Created!

📋 🔵 Basic — {days} Days

🗓 Expires:
{expire_date.strftime("%d-%m-%Y %H:%M:%S")} UTC

🔑 Keys:

"""

    for i, k in enumerate(generated, start=1):
        msg += f"{i}. {k}\n\n"

    bot.send_message(message.chat.id, msg)

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/check")
def check_key():

    key = request.args.get("key", "")

    if key in keys_db:

        return jsonify({
            "valid": True,
            "days": keys_db[key]["days"],
            "expires": keys_db[key]["expires"],
            "used": keys_db[key]["used"]
        })

    return jsonify({
        "valid": False
    })

@app.route("/activate")
def activate_key():

    key = request.args.get("key", "")

    if key in keys_db:

        keys_db[key]["used"] = True

        return jsonify({
            "success": True
        })

    return jsonify({
        "success": False
    })

def run_bot():
    bot.infinity_polling()

Thread(target=run_bot).start()

app.run(host="0.0.0.0", port=5000)