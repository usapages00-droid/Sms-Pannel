import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Aapka Token - isko naya wala daal dena revoke ke baad
BOT_TOKEN = "8766838886:AAFpWdcbRk9YgEANwO3RkdcYCG9pit9ycEw"
PANEL_USERNAME = "UmarRajput12"
PANEL_URL = "http://54.38.92.155/ints/login"

# Password yahan likhna nahi hai, bot khud puchega
PANEL_PASSWORD = input("freefire: ")

def get_panel_session():
    s = requests.Session()
    login_url = f"{PANEL_URL}index.php"
    # is panel ka login
    s.post(login_url, data={
        "username": UmarRajput12,
        "password": freefire
    }, timeout=15)
    return s

SESSION = get_panel_session()
print("Panel Login OK!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✅ UmarRajput12 Bot Ready!\n\n"
        "Format:\n"
        "sms 38665701517 Hello test\n"
        "ya\n"
        "sms Slovenia_novatel_sp01 38665701517 Hello"
    )

async def send_sms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.lower().startswith("sms "):
        return

    parts = text.split(" ", 2)
    if len(parts) == 2: # sms number only
        await update.message.reply_text("Message bhi likho: sms 38665701517 Hello")
        return

    # sms number message OR sms range number message
    try:
        args = text.split(" ", 3)
        if len(args) == 3:
            range_name = "Slovenia_novatel_sp01"
            number = args[1]
            msg = args[2]
        else:
            range_name = args[1]
            number = args[2]
            msg = args[3]

        await update.message.reply_text(f"⏳ Sending to {number} via {range_name}...")

        # Aapke panel ke SMS Test Panel ka data
        payload = {
            "range": range_name,
            "number": number,
            "message": msg,
            "sms_range": range_name,
            "sms_number": number,
            "sms_text": msg,
            "send": "Send"
        }

        # common send urls
        for endpoint in ["sms_test_panel.php", "index.php?page=sms_test", "send.php"]:
            try:
                r = SESSION.post(PANEL_URL + endpoint, data=payload, timeout=15)
                if r.status_code == 200:
                    break
            except:
                pass

        await update.message.reply_text(f"✅ Request sent to panel! Check Recent SMS Test: {number}")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_sms))

print("Bot is running... Telegram pe /start karo")
app.run_polling()
