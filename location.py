from telebot import types
from geopy.geocoders import Nominatim

class Geolocator:
    def __init__(self):
        self.geolocator = Nominatim(user_agent='why')
    
    def get_location_button(self):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_location = types.KeyboardButton(text="Здания поблизости", request_location=True)
        keyboard.add(button_location)
        return keyboard

    def get_location(self, message):
        if message.location is not None:
            long = message.location.longitude
            lat = message.location.latitude
            str_coordinates = str(lat) + ", " + str(long)
            location = self.geolocator.reverse(str_coordinates)
            return str_coordinates+location.address
        else:
            return 'Пожалуйста, включите геопозицию.'
