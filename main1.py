import os
import telebot
from flask import Flask, request
import uuid
import speech_recognition as sr

token = '5302345860:AAGahsIU7Q6lAYz4tD5ZVVFMpqugRKTHXIE'
app_url = f'https://spbuldings.herokuapp.com/{token}'
bot = telebot.TeleBot(token)
server = Flask(__name__)


@server.route('/' + token, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200


@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=app_url)
    return '!', 2000


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Yeah")
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


language = 'ru_RU'
r = sr.Recognizer()


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text, language=language)
            return text
        except:
            return "Sorry.. run again..."


@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full = "./voice/" + filename + ".ogg"
    file_name_full_converted = "./ready/" + filename + ".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system(os.path.abspath("ffmpeg") + " -i " +
              file_name_full + "  " + file_name_full_converted)
    text = recognise(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


bot.polling(none_stop=True, interval=0)
