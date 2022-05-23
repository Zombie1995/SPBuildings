import telebot
# Our modules
from webhook import Webhook
from location import Geolocator
from voice_recognition import VoiceRecognizer

WEBHOOK_URL = 'https://2fd0-188-243-183-20.ngrok.io'
API_TOKEN = '5302345860:AAGahsIU7Q6lAYz4tD5ZVVFMpqugRKTHXIE'

bot = telebot.TeleBot(API_TOKEN)
# Our classes
webhook = Webhook(bot, WEBHOOK_URL)
geolocator = Geolocator()
voice_recognizer = VoiceRecognizer()


@bot.message_handler(commands=["start"])
def start_msg(message):
    button = geolocator.get_location_button()
    text = ''
    text += 'Это инфа о боте \n'
    text += 'Еще одна инфа о боте'
    bot.send_message(
        message.chat.id, text,
        reply_markup=button)


@bot.message_handler(content_types=["location"])
def show_nearest(message):
    nearest = geolocator.get_nearest(message)
    bot.send_message(message.from_user.id, nearest)


@bot.message_handler(content_types=["voice"])
def recognize_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    voice_file = bot.download_file(file_info.file_path)
    text = voice_recognizer.get_text(voice_file)
    bot.send_message(message.from_user.id, text)


if __name__ == '__main__':
    webhook.run()
