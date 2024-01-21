import telebot
import logging
import os
import json
import time
from telethon import TelegramClient, events
import os
import asyncio
import joblib
import os
import torch
from torch.utils.data import Dataset
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
from transformers import DataCollatorForLanguageModeling
from transformers import Trainer, TrainingArguments
from supabase import create_client, Client
# from trainbot import build_model, get_response

# bot = telebot.TeleBot("6935474801:AAFi4WGxAQGnfy4I3y3GbaqmJrdiujCtU4g")
bot = telebot.TeleBot("6897672158:AAGQuVTrn_XZLSdoZAy-D-ujl3X9_gVyPJo")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
session_file = 'Jyothika_C.session'
api_id = '24468532'
api_hash = '12db7aeeabc14ee1b524422a8984b71e'
whitelist = ['Jyothika_C', 'raihahan', 'apollotan']

url: str = "https://jxkpnoxrzwybzxaindvb.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4a3Bub3hyend5Ynp4YWluZHZiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDU3MjM4MDEsImV4cCI6MjAyMTI5OTgwMX0.cVS-AMjZsmui6kQPviNgxpViach0lgRG1JeqYEDhhIY"
supabase: Client = create_client(url, key)

users = {}

# Create a custom PyTorch dataset
class ChatDataset(Dataset):
    def __init__(self, input_ids):
        self.input_ids = input_ids

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return {"input_ids": self.input_ids[idx]}

# Directory to store models
MODELS_DIR = "models"

def build_model(chat_data):
    # Load pre-trained GPT-2 model and tokenizer
    model_name = "gpt2"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    tokenizer.pad_token = " "

    # Tokenize and format the chat data
    input_ids = tokenizer(chat_data, return_tensors="pt", padding=True, truncation=True)["input_ids"]

    # Prepare the training dataset
    dataset = ChatDataset(input_ids)

    # Configure training settings
    training_args = TrainingArguments(
        output_dir="./gpt2-finetuned",
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=20,
        save_steps=10_000,
        save_total_limit=2,
    )

    # Use DataCollatorForLanguageModeling to handle padding
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )

    # Train the model
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()

    return model, tokenizer

def load_model(model_name):
    model_filename = f"/content/{MODELS_DIR}/{model_name}.joblib"
    vectorizer_filename = f"/content/{MODELS_DIR}/{model_name}_tokenizer.joblib"

    if os.path.exists(model_filename) and os.path.exists(vectorizer_filename):
        model = joblib.load(model_filename)
        vectorizer = joblib.load(vectorizer_filename)
        return model, vectorizer

def build_model_endpoint(txt_data, model_name):
    model, tokenizer = build_model(txt_data)

    # Save the model and vectorizer
    os.makedirs(MODELS_DIR, exist_ok=True)
    model_filename = f"{MODELS_DIR}/{model_name}.joblib"
    tokenizer_filename = f"{MODELS_DIR}/{model_name}_tokenizer.joblib"

    joblib.dump(model, model_filename)
    joblib.dump(tokenizer, tokenizer_filename)

    return f"Model '{model_name}' built and saved successfully"

def get_response(model_name, input_text):
    model, tokenizer  =  load_model('Jyothika_C')
    input_ids = tokenizer.encode(input_text, return_tensors="pt").to('cuda')

    # Generate response
    output_ids = model.generate(input_ids, max_length=100, num_beams=5, no_repeat_ngram_size=2, top_k=50, top_p=0.95, temperature=0.7)

    # Decode and print the generated response
    generated_response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_response

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the evil kermit bot!")

@bot.message_handler(commands=['setparams'])
def set_params(message):
    if message.text.strip() == "/setparams":
        bot.reply_to(message, "Please input params! Eg. /setparams jyothikac 6588888888")
        return
    parsed_input = message.text.split(" ")
    user_id = message.chat.id
    users[user_id] = {}
    users[user_id]['username'] = parsed_input[1]
    users[user_id]['phone'] = parsed_input[2]
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    users[user_id]['client'] = TelegramClient('Jyothika_C', api_id, api_hash, sequential_updates=True)
    bot.reply_to(message, "hi")

def get_phone_passcode(username: str) -> str:
    timeout_limit = 120
    timeout_curr = 0

    while timeout_curr <= timeout_limit:
        data = supabase.from_("login_passcode") \
                        .select("login_passcode") \
                        .eq("username", username) \
                        .limit(1) \
                        .execute()
        if data.data is not None:
            if len(data.data) == 1:
                login_passcode = data.data[0]["login_passcode"]
                if login_passcode is not None:
                    supabase.from_("login_passcode") \
                            .delete() \
                            .eq("username", username) \
                            .execute()
                    print("Passcode: ", login_passcode)
                    return login_passcode
        print("waiting for login passcode for ", username, "...")      
        time.sleep(5)
        timeout_curr += 5
    
    return ""

@bot.message_handler(commands=['startclient'])
def start_client(message):
    user_id = message.chat.id
    client = users[user_id]['client']
    @client.on(events.NewMessage(incoming=True))
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
                message = "hello world"
                await event.respond(message)
    print(time.asctime(), '-', 'Auto-replying...')
    loop = asyncio.new_event_loop()
    # def code_callback(username):
    #   # Run the synchronous function in a separate thread
    #   result = loop.run_in_executor(None, lambda : get_phone_passcode(username))
    #   return result
    asyncio.set_event_loop(loop)
    client.start(users[user_id]['phone'], code_callback=lambda : get_phone_passcode(message.from_user.username))
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')
    # for message in client.iter_messages('raihahan',reverse=True):
    #     print(message.sender_id, ':', message.text)

    chat_txt = ""

    for message in client.iter_messages('raihahan',reverse=True):
        chat_txt  += str(message.sender_id) + ':' + message.text

    build_model_endpoint(chat_txt, 'Jyothika_C')

    print(get_response('Jyothika_C', "Hi, how are you?"))
    client.run_until_disconnected()
    print(time.asctime(), '-', 'Stopped!')



@bot.message_handler(commands=['trainbot'])
def train_bot(message):
    return

@bot.message_handler(commands=['otp'])
def otp(message):
    username = message.from_user.username
    parsed_input = message.text.split(" ")
    passcode = parsed_input[1]
    passcode = passcode[::-1]
    try:
      supabase.from_("login_passcode") \
              .insert({ "username": username, "login_passcode": passcode }) \
              .execute()
      return { "message": "Success!" }
    except Exception as e:
      print(e)


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()