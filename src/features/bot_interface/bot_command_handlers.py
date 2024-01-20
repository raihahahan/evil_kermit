from telegram.ext import ContextTypes
from telegram import Update
from features.bot_interface import bot_resources
from features.bot_interface import bot_utils

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_resources.START)

async def clone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_handle = bot_utils.extract_telegram_handle(update.message.text)
    print(telegram_handle)