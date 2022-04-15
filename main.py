import telebot
bot = telebot.TeleBot('5302345860:AAGahsIU7Q6lAYz4tD5ZVVFMpqugRKTHXIE')

name = ''
surname = ''
age = 0
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Yeah")
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')


bot.polling(none_stop=True, interval=0)