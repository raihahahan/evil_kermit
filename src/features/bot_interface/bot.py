from dotenv import load_dotenv
import time
from telethon import TelegramClient, events
import os
from features.bot_interface.bot_utils import respond_from_message, get_phone_passcode
from typing import List
import asyncio

load_dotenv()

class Bot():
    def __init__(self, username: str, phone: str, whitelist: List[str]):
        self.username = username
        self.phone = phone
        self.whitelist = whitelist
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        self.client = TelegramClient(username, api_id, api_hash, sequential_updates=True)
        self.loop = asyncio.get_event_loop()

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

        def code_callback(self, username):
            # Run the synchronous function in a separate thread
            result = self.loop.run_in_executor(None, lambda : get_phone_passcode(username))
            return result

        await self.client.start(self.phone, code_callback=lambda : code_callback(self, self.username))
        await self.client.run_until_disconnected()
        print(time.asctime(), '-', 'Stopped!')

    async def stop(self):
        root_directory = os.getcwd()
        for file_name in os.listdir(root_directory):
            if file_name == f"{self.username}.session":
                file_path = os.path.join(root_directory, file_name)
                os.remove(file_path)
                print(f"Removed: {file_path}")
                break
        await self.client.disconnect()







