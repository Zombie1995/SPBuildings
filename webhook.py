import time
import telebot
import flask

APP_HOST = '127.0.0.1'
APP_PORT = '5000'


class Webhook:
    def __init__(self, bot, webhook_url):
        self.app = flask.Flask(__name__)
        bot.remove_webhook()
        time.sleep(1)
        bot.set_webhook(url=webhook_url)

        @self.app.route('/', methods=['POST'])
        def webhook():
            if flask.request.headers.get('content-type') == 'application/json':
                json_string = flask.request.get_data().decode('utf-8')
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])
                return '!', 200
            else:
                flask.abort(403)

    def run(self):
        self.app.run(host=APP_HOST, port=APP_PORT, debug=True)
