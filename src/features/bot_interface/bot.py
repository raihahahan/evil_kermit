from dotenv import load_dotenv
import time
from telethon import TelegramClient, events
import os
from features.bot_interface.bot_utils import respond_from_message, get_phone_passcode
from typing import List

load_dotenv()

class Bot():
    def __init__(self, username: str, phone: str, whitelist: List[str]):
        self.username = username
        self.phone = phone
        self.whitelist = whitelist
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        self.client = TelegramClient(username, api_id, api_hash, sequential_updates=True)

    async def start(self):        
        @self.client.on(events.NewMessage(incoming=True))
        async def handle_new_message(event):
            if event.is_private:  # only auto-reply to private chats
                sender = await event.get_sender()
                from_ = await event.client.get_entity(event.from_id)  # this lookup will be cached by telethon
                if not from_.bot and sender.username in self.whitelist:  # don't auto-reply to bots
                    print("------")
                    print(time.asctime(), '-', event.message)  # optionally log time and message
                    print("Message is: ", event.message.message)
                    time.sleep(1)  # pause for 1 second to rate-limit automatic replies
                    sender_message = event.message.message
                    message = respond_from_message(sender_message)
                    await event.respond(message)

        print(time.asctime(), '-', 'Auto-replying...')

        await self.client.start(self.phone, code_callback=lambda : get_phone_passcode(self.username))
        await self.client.run_until_disconnected()
        print(time.asctime(), '-', 'Stopped!')

    async def stop(self):
        await self.client.disconnect()







