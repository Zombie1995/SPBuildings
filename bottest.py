import telebot
from telebot import types

bot = telebot.TeleBot('5362978044:AAFFiVObDWbmOpzuP1lvSh_F_ZdDtBhYLTw')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Найти здания поблизости 🌎')
    btn2 = types.KeyboardButton('Техническая поддержка 🤖')
    btn3 = types.KeyboardButton('О боте 💀')
    markup.add(btn1)
    markup.add(btn2, btn3)
    bot.send_message(message.chat.id, text='Привет, {0.first_name}! Я виртуальный экскурсовод SPBuildings!'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == 'Найти здания поблизости 🌎'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('1️⃣')
        btn2 = types.KeyboardButton('2️⃣')
        btn3 = types.KeyboardButton('3️⃣')
        btn4 = types.KeyboardButton('4️⃣')
        btn5 = types.KeyboardButton('5️⃣')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        markup.add(btn4)
        markup.add(btn5)
        back = types.KeyboardButton('Вернуться в главное меню')
        markup.add(back)
        bot.send_message(message.chat.id, text='В процессе...', reply_markup=markup)

    elif (message.text == 'Техническая поддержка 🤖'):
        bot.send_message(message.chat.id, text='@theorly')

    elif (message.text == 'О боте 💀'):
        bot.send_message(message.chat.id, text='Данный бот способен помочь определиться на местности, \n'
                                               'а также показать интересные места вокруг!')

    elif (message.text == 'Вернуться в главное меню'):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Найти здания поблизости 🌎')
        btn2 = types.KeyboardButton('Техническая поддержка 🤖')
        btn3 = types.KeyboardButton('О боте 💀')
        markup.add(btn1)
        markup.add(btn2, btn3)
        bot.send_message(message.chat.id, text='Вы вернулись в главное меню', reply_markup=markup)

    else:
        bot.send_message(message.chat.id, text='Я не знаю, что ответить..')

bot.polling(none_stop=True)

