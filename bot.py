import telebot
from flask import Flask, request, render_template
import get_prediction

from PIL import Image
from io import BytesIO
import os

TOKEN = '1693842857:AAE9jPzrMWS93DZ0FM1DqRPZj3bsOMZnskI'
bot = telebot.TeleBot(TOKEN)


# command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_first_name = message.from_user.first_name
    bot.reply_to(message, f"Welcome {user_first_name}, I'm HotDog or not HotDog bot 🤖 \n"
                          f"Send me a photo to see if it is a hot dog 🌭")


# text handler
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет" or message.text == "привет":
        bot.send_message(message.from_user.id, "Howdy, human!")
    else:
        bot.reply_to(message.from_user.id, 'Send me a photo to see if it is a hot dog 🌭')


# photo handler to make prediction
@bot.message_handler(content_types=['photo'])
def send_prediction_on_photo(message):
    # get photo id and upload it into memory
    photo_id = message.photo[-1].file_id  # [-1] index corresponds to the best quality
    photo_info = bot.get_file(photo_id)
    photo_bytes = bot.download_file(photo_info.file_path)
    bot.send_message(message.chat.id, 'Your photo is in line, please wait.')
    pil_img = Image.open(BytesIO(photo_bytes))  # create BytesIO wrapper for the image

    prediction = get_prediction.lets_rock(pil_img)

    # send prediction with probability
    if prediction:
        bot.send_message(message.chat.id, '🌭🌭🌭 Yayyy! It is a hot dog 🌭🌭🌭')
    else:
        bot.send_message(message.chat.id, '🤡🤡🤡 Ooops! It is not a hot dog 🤡🤡🤡')


bot.polling(none_stop=True)
