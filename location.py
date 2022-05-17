import telebot
import requests
from telebot import types
from geopy.geocoders import Nominatim

bot = telebot.TeleBot('5302345860:AAGahsIU7Q6lAYz4tD5ZVVFMpqugRKTHXIE')
geolocator = Nominatim(user_agent='why')


@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_location = types.KeyboardButton(text="Поделиться местоположением", request_location=True)
    keyboard.add(button_location)
    bot.send_message(message.chat.id, "Поделитесь вашим местоположением (должна быть включена геолокация) ",
                     reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    if message.location is not None:
        print(message.location)
        print(message)
        long = message.location.longitude
        lat = message.location.latitude
        str_coordinates = str(lat) + ", " + str(long)
        location = geolocator.reverse(str_coordinates)
        print(location.address)


bot.polling(none_stop=True, interval=0)
