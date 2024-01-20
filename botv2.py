import telebot
import logging
import os
import json
import time
from telethon import TelegramClient, events
import os

bot = telebot.TeleBot("6935474801:AAFi4WGxAQGnfy4I3y3GbaqmJrdiujCtU4g")
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
session_file = 'Jyothika_C.session'
api_id = '24468532'
api_hash = '12db7aeeabc14ee1b524422a8984b71e'

users = {}

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
    users[user_id]['phonenumber'] = parsed_input[2]
   # users[user_id]['client'] = TelegramClient(session_file, api_id, api_hash, sequential_updates=True)
    print(users[user_id])
    

# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" + m.text + "\"\nMaybe try the help page at /help")

bot.polling()