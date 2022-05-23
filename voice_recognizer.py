import telebot
import uuid
import os
import speech_recognition as sr
# bot = telebot.TeleBot('5302345860:AAGahsIU7Q6lAYz4tD5ZVVFMpqugRKTHXIE')
bot = telebot.TeleBot('1644030482:AAG_p9fN77Q2T0Nxjbqm53zjm9vkHUNI9-8')


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Yeah")
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


language = 'ru_RU'
r = sr.Recognizer()


def recognize(filename):
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
    file_name_full = "./voice/"+filename+".ogg"
    file_name_full_converted = "./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system(os.path.abspath("ffmpeg") + " -i " +
              file_name_full+"  "+file_name_full_converted)
    text = recognize(file_name_full_converted)
    bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)


bot.polling(none_stop=True, interval=0)
