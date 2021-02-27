import logging
from pprint import pprint
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import config
from mastermind_engine import check_number, get_turns, make_number

logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = config.TOKEN


def main_keyboard():
    return ReplyKeyboardMarkup([
         ['Загадывай!', 'Сдаюсь!', 'Помощь'],

    ])


def greet_user(update, context):
    print('вызван start')
    update.message.reply_text(f'Привет, давай сыграем в игру  {config.RULES_URL}', reply_markup=main_keyboard())


def help_user(update, context):
    print('вызван help')
    update.message.reply_text(f'Bulls это количество цифр в твоем ответе, которое ты поставил на правильное место.\n\n'
                              f'Cows это количество цифр в твоем ответе, которые есть в загаданном числе, но ты их поставил не на то место\n\n'
                              f'Например, загадано число 1234\n'
                              f'Мы пишем боту 2574\n\n'
                              f'2 - есть в загаданном числе 1234, но она стоит не на первом месте, а на втором. Значит она будет считаться в Cows\n'
                              f'5 и 7 нет в загаданном числе - они не считаются\n\n'
                              f'А вот 4 есть и мы поставили ее на правильное место\n'
                              f'Она будет засчитана в Bulls\n\n'
                              f'Ответ бота будет: Bulls: 1, Cows 1\n')


def check_number_v2(message, number):
    bulls_cows = {'bulls': 0, 'cows': 0}

    if len(str(message)) > 4:
        return 'too long string'

    elif not str(message).isnumeric():
        return 'wrong input'

    elif int(message) == int(number):
        return 'win'

    else:
        for order, digit in enumerate(message):
            if digit in number:
                if number[order] == digit:
                    bulls_cows['bulls'] += 1
                else:
                    bulls_cows['cows'] += 1

        return bulls_cows


def send_text(update, context):
    print('вызван send text')
    message = update.message.text
    chat_id = update.effective_chat.id

    if message == 'Загадывай!':
        if context.user_data.get('number', 0):
            update.message.reply_text(f'Уже загадано', reply_markup=main_keyboard())
        else:
            number = make_number()
            context.user_data['number'] = number
            context.user_data['turns'] = 0
            print(f'Чат {chat_id}, Загадано {number}')
            update.message.reply_text('Загадано, угадывай!', reply_markup=main_keyboard())

    elif message == 'Сдаюсь!':
        if context.user_data:
            reply = f'Ты сдался на {context.user_data.get("turns", 0)} попытке.\nБыло загадано число {context.user_data["number"]}'
            context.user_data['number'] = ''
            context.user_data['turns'] = 0
        else:
            reply = choice(['Не сдавайся!', 'Never give in!', 'Всё в ваших руках, поэтому не стоит их опускать'])
        update.message.reply_text(reply, reply_markup=main_keyboard())

    else:
        number = context.user_data.get('number', make_number())
        reply = check_number_v2(message, number)
        context.user_data['turns'] += 1
        current_turns = context.user_data['turns']

        if reply == 'wrong input':
            update.message.reply_text('Wrong input: need 4 digits, but symbols were given.')

        elif reply == 'win':
            context.user_data['number'] = make_number()
            context.user_data['turns'] = 0
            update.message.reply_text(f'Ты победил в {current_turns} попыток', reply_markup=main_keyboard())

        elif reply == 'too long string':
            update.message.reply_text('Too long string. Need 4 digits.')

        elif isinstance(reply, dict):
            # context.user_data['last_user_turn'] = message
            # context.user_data['last_bulls_cows'] = reply
            reply_message = f'Bulls {reply["bulls"]}, Cows {reply["cows"]}'
            update.message.reply_text(reply_message, reply_markup=main_keyboard())

        else:
            update.message.reply_text('something goes wrong! Please screenshot to @Rom762', reply_markup=main_keyboard())


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Помощь)$pip install psycopg2-binarypip install psycopg2-binarypip install psycopg2-binarypip install psycopg2-binary'), help_user))
    dp.add_handler(MessageHandler(Filters.text, send_text))

    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()





