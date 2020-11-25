from pprint import pprint
import telebot
import config
from mastermind_engine import check_number, get_turns

import oop_engine

import logging

#logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.

bot = telebot.TeleBot(config.TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    pprint(message)

@bot.message_handler(func=lambda m: True)
def start(message):
    user_text = message.text
    chat_id = message.chat.id
    #print(begin_text, type(begin_text), message.chat.id)
    print('=====================================')

    answer = list(check_number(user_text, chat_id))
    if str(answer[0]) == 'wrong':
        bot_message = 'Wrong number'

    elif str(answer[0]) == 'win':
        bot_message = 'You win!'

    elif str(answer[0]) == 'help':
        bot_message = f'Help: {answer[1]}'
    else:
        bot_message = f'bulls: {answer[0]}, cows: {answer[1]}'

    print(f'Шаг: {get_turns()}, Чат: {message.chat.id}, Сообщение: {message.text}')

    bot.reply_to(message, bot_message)

bot.polling()






