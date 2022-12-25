#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

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

# Modes of printing the stations
WT, NWT = range(2)

TBOTID = os.environ['TBOTID']
TBOTKEY  = os.environ['TBOTKEY']

updater = Updater("{}:{}".format(TBOTID, TBOTKEY))

# Generate human readable message of a given station
def formatStation(station, mode):
    reply = "🚏 __*{}*__ - {}\n".format(station['Description'], station['CustomerCode'])

    for line in station['Lines']:
        if(mode == WT):
            reply = reply + "\n🚌 *{}* - *{}* - {}".format(line['Line']['LineCode'].replace('-','M'), line['WaitMessage'], line['Line']['LineDescription'])
        else:
            reply = reply + "\n🚌 *{}* - {}".format(line['Line']['LineCode'].replace('-','M'), line['Line']['LineDescription'])

    return reply

def hello(update, context):
    update.message.reply_text('Hello {}'.format(update.message.from_user.first_name))
    return SEARCH

def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text("Bye! I hope we can talk again some day.")

    return ConversationHandler.END

def findInResults(stationCode, results):
    for index, s in enumerate(results):
        if s['CustomerCode'] == stationCode:
            return index
    return -1

def search(update, context):
    results = atm.searchStop(update.message.text)
    logger.info('message - '+ update.message.text)

    #No result case
    if (len(results) == 0):
        update.message.reply_text("No results found")
        return ConversationHandler.END

    # Many results
    index = findInResults(update.message.text, results)
    if (index > -1): # Exact match
        update.message.reply_text("Looking for the waiting time ...")
        station = atm.getWaitingTime(results[index]['Code'])
        context.bot.send_message(chat_id=update.message.chat_id,
                         text=formatStation(station, WT),
                         parse_mode=ParseMode.MARKDOWN)
        context.bot.send_venue(chat_id=update.message.chat_id,
                         latitude=station['Location']['Y'],
                         longitude=station['Location']['X'],
                         title=station['Description'],
                         address=station['Address'])
        return ConversationHandler.END
    
    else: # Partial match 
        update.message.reply_text("I found {} stations, send code for wating times".format(len(results)));
        for station in results:
            context.bot.send_message(chat_id=update.message.chat_id,
                             text=formatStation(station, NWT),
                             parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END

conv_handler = ConversationHandler(
entry_points=[MessageHandler(Filters.text, search)],
states={
    #SEARCH : [MessageHandler(Filters.text, search)]
},
fallbacks=[CommandHandler('cancel', cancel)])

updater.dispatcher.add_handler(conv_handler)
updater.start_polling()
updater.idle()
