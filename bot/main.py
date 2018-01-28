#!/usr/bin/env python

import io
import os

import telegram
from flask import Flask, request, current_app

from telegram.ext import Dispatcher, CommandHandler

from utils import Utils

TOKEN = os.getenv('TOKEN')
SOURCE_TOKEN = os.getenv('SOURCE_TOKEN', "")
HOST = os.getenv('HOST')  # Same FQDN used when generating SSL Cert
PORT = os.getenv('PORT', 8443)
CERT = os.getenv('CERT')
CERT_KEY = os.getenv('CERT_KEY')
CERT_STR = os.getenv('CERT_STR')
PERMANENT_CHATS = os.getenv('PERMANENT_CHATS')  # Comma separated ids wrapped in a string
OWNER_ID = os.getenv('OWNER_ID')

ADMIN_LEVEL = 1  # 1=Channel admins + Owner, 2=Channel admins, 3=Owner only

telegram_bot = telegram.Bot(TOKEN)

app = Flask(__name__)


@app.route('/' + SOURCE_TOKEN, methods=['POST'])
def relay():
    with app.app_context():
        muted = current_app.muted
        chats = current_app.chats
    if not muted:
        json = request.get_json(force=True)
        for chat in chats:
            chat_id = telegram_bot.get_chat(chat).id
            utils.send_message(chat_id=chat_id, text=json['message'])
        return "OK"
    return "MUTED"


@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    update = telegram.update.Update.de_json(request.get_json(force=True), telegram_bot)

    utils.set_update(update)
    bot_dispatcher.process_update(update)
    return "OK"


class BotDispatcher:
    def __init__(self):
        self.dispatcher = Dispatcher(telegram_bot, None, workers=0)
        self.dispatcher.add_handler(CommandHandler('register', register))
        self.dispatcher.add_handler(CommandHandler('unregister', unregister))
        self.dispatcher.add_handler(CommandHandler('mute', mute))
        self.dispatcher.add_handler(CommandHandler('unmute', unmute))

    def process_update(self, update):
        self.dispatcher.process_update(update)


def register(bot, update):
    if has_permission():
        with app.app_context():
            chats = current_app.chats

        chat = utils.get_message().chat
        if str(chat.id) not in chats:
            chats.append(str(chat.id))

        with app.app_context():
            current_app.chats = chats

        utils.send_message(chat_id=chat.id,
                           text="Registered <code>{}</code> to receive updates".format(chat.title))
    else:
        permission_denied()


def unregister(bot, update):
    if has_permission():
        with app.app_context():
            chats = current_app.chats

        chat = utils.get_message().chat
        if str(chat.id) in chats:
            chats.remove(str(chat.id))

        with app.app_context():
            current_app.chats = chats

        utils.send_message(chat_id=utils.get_chat().id,
                           text="Unregistered <code>{}</code>. Bye!".format(utils.get_chat().title))

        chat.leave()

    else:
        permission_denied()


def mute(bot, update):
    if has_permission() or utils.is_chat_private():
        toggle_mute(True)
    else:
        permission_denied()


def unmute(bot, update):
    if has_permission() or utils.is_chat_private():
        toggle_mute(False)
    else:
        permission_denied()


def toggle_mute(is_muted):
    with app.app_context():
        current_app.muted = is_muted

    muted_str = "off"
    if is_muted:
        muted_str = "on"

    utils.send_message(chat_id=utils.get_chat().id,
                       text="Turning <code>mute</code> <b>{}</b>".format(muted_str))


def has_permission():
    if ADMIN_LEVEL == 1:
        return utils.is_user_admin() or utils.is_chat_all_admins() or utils.matches_user_id(OWNER_ID)
    elif ADMIN_LEVEL == 2:
        return utils.is_user_admin() or utils.is_chat_all_admins()
    elif ADMIN_LEVEL == 3:
        return utils.matches_user_id(OWNER_ID)


def permission_denied():
    utils.send_message(chat_id=utils.get_chat().id,
                       reply_to_message_id=utils.get_message().message_id,
                       text="You're not my mom!")


def set_webhook():
    if CERT_STR:
        cert = io.StringIO(CERT_STR)
    else:
        cert = open(CERT, 'rb')

    telegram_bot.set_webhook(url='https://%s:%s/%s' % (HOST, PORT, TOKEN),
                             certificate=cert)


def init():
    set_webhook()

    chats = PERMANENT_CHATS.split(',')

    with app.app_context():
        current_app.muted = False
        try:
            current_app.chats = chats
        except AttributeError:
            current_app.chats = []

    if not SOURCE_TOKEN:
        print("SOURCE_TOKEN required to receive relays")
        exit()

    print("Added {} chats on start {}".format(len(chats), chats))

    params = {
        'host': '0.0.0.0',
        'port': int(PORT)
    }

    if CERT and CERT_KEY:
        params['ssl_context'] = (CERT, CERT_KEY)

    return params


bot_dispatcher = BotDispatcher()
utils = Utils(telegram_bot)


app_params = init()


if __name__ == '__main__':
    app.run(**app_params)
