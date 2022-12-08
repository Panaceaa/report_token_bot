# coding=utf-8
import datetime
import io
import pdf_creator
from telegram.ext import Updater, filters
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import re

token = '5885210159:AAEdEUQrcv7AG2SspuCEF4frkObNNMuVQHw'
chat_ids = [3425582, 386176193, 2134848305]
updater = Updater(token, use_context=True)


"############################### Bot ############################################"


def start(update, context):
    chat_id = update.message.chat.id

    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard())


def main_menu(update, context):
    chat_id = update.callback_query.message.chat.id
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text=main_menu_message(),
        reply_markup=main_menu_keyboard())


def clients_menu(update, context):
    chat_id = update.callback_query.message.chat.id
    query = update.callback_query
    context.user_data['head_lvl'] = query.data
    query.answer()
    if 'b4bm' in context.user_data['head_lvl']:
        file = pdf_creator.file_creator('B4BM')
        context.bot.send_document(chat_id, file)

    elif 'b4bo' in context.user_data['head_lvl']:
        file = pdf_creator.file_creator('B4BO')
        context.bot.send_document(chat_id, file)


"############################ Keyboards #########################################"


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('B4BM', callback_data='b4bm')],
                [InlineKeyboardButton('B4BO', callback_data='b4bo')]]
    return InlineKeyboardMarkup(keyboard)


def clients(character):
    keyboard = [[InlineKeyboardButton('Назад', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


"############################# Messages #########################################"


def main_menu_message():
    return 'По какому токену нужен отчет?'


"############################# Handlers #########################################"


TICKER, DATE, START_PRICE, CLOSE_DATE, CLOSE_PRICE, TRANSACTION, QUANTITY = range(7)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(clients_menu, pattern='b4bm'))
updater.dispatcher.add_handler(CallbackQueryHandler(clients_menu, pattern='b4bo'))


updater.start_polling()