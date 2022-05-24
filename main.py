from random import randint
import telebot
from image_parsing import YandexImage
# Our modules
from webhook import Webhook
from location import Geolocator
from voice_recognition import VoiceRecognizer

WEBHOOK_URL = 'https://c361-188-243-183-20.ngrok.io'
API_TOKEN = '5302345860:AAGahsIU7Q6lAYz4tD5ZVVFMpqugRKTHXIE'

bot = telebot.TeleBot(API_TOKEN)
image_parser = YandexImage()
# Our classes
webhook = Webhook(bot, WEBHOOK_URL)
geolocator = Geolocator()
voice_recognizer = VoiceRecognizer()

# Nearest buildings
nearest = []


@bot.message_handler(commands=["start"])
def start_msg(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton(
        'Найти здания поблизости 🌎', request_location=True)
    btn2 = telebot.types.KeyboardButton('Техническая поддержка 🤖')
    btn3 = telebot.types.KeyboardButton('О боте 💀')
    markup.add(btn1)
    markup.add(btn2, btn3)
    text = ''
    text += f'Привет, {message.from_user.first_name}!\n'
    text += 'Я виртуальный экскурсовод SPBuildings!'
    bot.send_message(
        message.chat.id, text,
        reply_markup=markup)


@bot.message_handler(content_types=["location"])
def show_nearest(message):
    global nearest
    nearest = geolocator.get_nearest(message)
    if len(nearest) == 0:
        bot.send_message(
            message.chat.id,
            'Исторические здания рядом не обнаружены.')
        return
    building_index = 0
    for building in nearest:
        name = building['name']
        address = building['address']
        text = '🏠 ' + name
        btn = telebot.types.InlineKeyboardButton(
            text, callback_data=str(building_index))
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(btn)
        img_url = image_parser.search(
            name + ' ' + address)[randint(0, 5)].preview.url
        message_id = bot.send_photo(
            message.chat.id, img_url,
            reply_markup=markup).message_id
        building['message_id'] = message_id
        building_index += 1


@bot.callback_query_handler(func=lambda call: True)
def building_history(call):
    chat_id = call.message.chat.id
    building_index = int(call.data)
    bot.edit_message_reply_markup(
        chat_id,
        message_id=nearest[building_index]['message_id'],
        reply_markup=None)
    for i in range(len(nearest)):
        if i != building_index:
            message_id = nearest[i]['message_id']
            bot.delete_message(chat_id, message_id)
    text = ''
    text += nearest[building_index]['name'] + '\n'
    text += '(' + nearest[building_index]['address'] + ')' + '\n'
    text += nearest[building_index]['history']
    bot.send_message(chat_id, text)


@bot.message_handler(content_types=["voice"])
def recognize_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    voice_file = bot.download_file(file_info.file_path)
    text = voice_recognizer.get_text(voice_file).capitalize()
    if 'Расскажи' in text:
        reply_text = ''
        reply_text = 'Команда распознана, но, к сожалению, '
        reply_text = 'Такого функционала пока нет((('
        bot.send_message(message.from_user.id, reply_text)
    else:
        bot.send_message(message.from_user.id,
                         'Голосовая команда не распознана')


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == 'Техническая поддержка 🤖'):
        bot.send_message(message.chat.id, text='@theorly')

    elif (message.text == 'О боте 💀'):
        text = ''
        text += 'Данный бот поможет определиться на местности, '
        text += 'а также показать интересные места вокруг!\n'
        text += 'Используйте голосовую команду "Расскажи мне о...", '
        text += 'чтобы узнать историю известного вам здания.'
        bot.send_message(message.chat.id, text)

    elif (message.text == 'Вернуться в главное меню'):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton(
            'Найти здания поблизости 🌎', request_location=True)
        btn2 = telebot.types.KeyboardButton('Техническая поддержка 🤖')
        btn3 = telebot.types.KeyboardButton('О боте 💀')
        markup.add(btn1)
        markup.add(btn2, btn3)
        bot.send_message(
            message.chat.id, text='Вы вернулись в главное меню',
            reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text='Я не знаю, что ответить..')


if __name__ == '__main__':
    webhook.run()
