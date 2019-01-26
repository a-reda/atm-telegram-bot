#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import os
import re
import json

import atm

import logging
import settings

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SEARCH, RESULT = range(2)

TBOTID = os.environ['TBOTID']
TBOTKEY  = os.environ['TBOTKEY']

updater = Updater("{}:{}".format(TBOTID, TBOTKEY))


# Generate human readable message of a given station
def formatStation(station):
    reply = "{} - {}\n".format(station['CustomerCode'], station['Description'])

    for line in station['Lines']:
        reply = reply + "\n{} - {} - {}".format(line['Line']['LineCode'], line['WaitMessage'], line['Line']['LineDescription'])

    return reply

def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
    return SEARCH

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("Bye! I hope we can talk again some day.")

    return ConversationHandler.END

def search(bot, update):
    res = atm.searchStop(update.message.text)

    if (len(res) == 1):
        update.message.reply_text("I will give you the waiting time")
        result = atm.getWaitingTime(res[0]['Code'])
        update.message.reply_text(formatStation(result))
        return ConversationHandler.END
    elif (len(res) == 0):
        update.message.reply_text("No result found")
        return ConversationHandler.END
    else:
        update.message.reply_text("I found {}".format(len(res)));

    return ConversationHandler.END

conv_handler = ConversationHandler(
entry_points=[MessageHandler(Filters.text, hello)],
states={
    SEARCH : [MessageHandler(Filters.text, search)]
},
fallbacks=[CommandHandler('cancel', cancel)])

updater.dispatcher.add_handler(conv_handler)

updater.start_polling()
updater.idle()
