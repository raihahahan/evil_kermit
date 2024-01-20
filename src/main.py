from features.bot_interface.bot import Bot
import os
from features.bot_interface.bot_utils import get_phone_passcode

def main():
    bot = Bot(phone=os.getenv("PHONE"), username=os.getenv("SESSION_FILE"))
    bot.start()

if __name__ == "__main__":
    main()