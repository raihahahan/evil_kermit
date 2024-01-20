from dotenv import load_dotenv
import telegram
import os
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from telegram import Update
import logging 

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

class Bot():
    def __init__(self):
        self.bot = ApplicationBuilder().token(os.getenv("BOT_API")).build()

    def run(self):
        start_handler = CommandHandler('start', start)
        self.bot.add_handler(start_handler)
        self.bot.run_polling()




