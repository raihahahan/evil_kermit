from dotenv import load_dotenv
import os
from telegram.ext import ApplicationBuilder, CommandHandler
import logging 
from features.bot_interface import bot_command_handlers

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class Bot():
    def __init__(self):
        self.bot = ApplicationBuilder().token(os.getenv("BOT_API")).build()

    def run(self):
        start_handler = CommandHandler('start', bot_command_handlers.start)
        clone_handler = CommandHandler('clone', bot_command_handlers.clone)

        # add handlers
        self.bot.add_handler(start_handler)
        self.bot.add_handler(clone_handler)

        # start polling
        self.bot.run_polling()






