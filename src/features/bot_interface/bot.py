from dotenv import load_dotenv
import time
from telethon import TelegramClient, events
import os
from features.bot_interface.bot_utils import respond_from_message, whitelist
from telethon.tl.functions.messages import (GetHistoryRequest)
import datetime

load_dotenv()

class Bot():
    def __init__(self):
        session_file = os.getenv("SESSION_FILE")
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        self.client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)

    def get_chat_history(self, person):
        messages = self.client.iter_messages(person,reverse=True)
        # Open text file in write+text mode
        text_file = open("sample.txt", "wt")

        # Write content to file
        for message in messages:
            n = text_file.write(str(message.peer_id.user_id) + ":" + message.message +  "\n")

            if n == len(message.message):
                print("Success! String written to text file.")
            else:
                print("Failure! String not written to text file.")

        # Close file
        text_file.close()
        

    def start(self):        
        phone = os.getenv("PHONE")
        password = os.getenv("PASSWORD")
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            if event.is_private:  # only auto-reply to private chats
                sender = await event.get_sender()
                from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
                if not from_.bot and sender.username in whitelist:  # don't auto-reply to bots
                    print("------")
                    print(time.asctime(), '-', event.message)  # optionally log time and message
                    print("Message is: ", event.message.message)
                    time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                    sender_message = event.message.message
                    message = respond_from_message(sender_message)
                    await event.respond(message)

        print(time.asctime(), '-', 'Auto-replying...')
        self.client.start(phone, password)
        self.get_chat_history('apollotan')
        self.client.run_until_disconnected()
        print(time.asctime(), '-', 'Stopped!')







