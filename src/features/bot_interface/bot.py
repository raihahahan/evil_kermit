from dotenv import load_dotenv
import time
from telethon import TelegramClient, events
import os
from features.bot_interface.bot_utils import respond_from_message, get_phone_passcode, get_whitelist

load_dotenv()

class Bot():
    def __init__(self, username, phone):
        self.username = username
        self.phone = phone
        self.whitelist = get_whitelist(username)
        api_id = os.getenv("API_ID")
        api_hash = os.getenv("API_HASH")
        self.client = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)

    async def get_chat_history(self):
        messages = await self.client.get_messages('Jyothika_C', limit=10)
        print(messages)
        return messages

    def start(self):        
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
        self.client.start(phone, password)
        for message in self.client.iter_messages('raihahan',reverse=True):
            print(message.sender_id, ':', message.text)
        self.client.run_until_disconnected()
        print(time.asctime(), '-', 'Stopped!')

    def stop(self):
        self.client.disconnect()







