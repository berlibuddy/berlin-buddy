import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# =============== CONFIGURAZIONE ===============
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in environment variables")

# =============== LOGGING ===============
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# =============== IL CUORE DEL BOT ===============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "there"
    welcome_text = (
    f"Moin {user_name}! 👋\n\n"
    "I'm Buddy — your expat wingman in Berlin.\n\n"
    "Trying to get an **Anmeldung appointment** at the Bürgeramt?\n"
    "Yeah… the website is chaos. 😅\n\n"
    "I watch the official site every few minutes.\n"
    "When a slot appears, I alert you instantly.\n\n"
    "No more refreshing.\n"
    "No more F5 madness.\n\n"
    "Ready to hunt your Anmeldung slot? 👇"
)
    await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

# =============== SETUP DEL BOT ===============
def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    logger.info("🤖 Berlin Buddy is starting... listening for messages.")
    app.run_polling()

# =============== FLASK PER TENERE VIVO RENDER ===============
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "🤖 Berlin Buddy is alive and kicking!"

@flask_app.route('/health')
def health():
    return "OK", 200

def run_flask():
    flask_app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

# =============== PUNTO DI ENTRATA PRINCIPALE ===============
if __name__ == "__main__":
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 Flask health check server started.")
    run_bot()
