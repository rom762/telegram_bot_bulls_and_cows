import sqlalchemy

import config
import datetime
import logging
from pprint import pprint
from random import choice, randint
from telegram import ReplyKeyboardMarkup, Chat
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


# logging.basicConfig(filename='bulls_and_cows_bot.log', level=logging.INFO)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename='bulls_and_cows_bot.log'
)

logger = logging.getLogger(__name__)

TOKEN = config.TOKEN


def main_keyboard():
    return ReplyKeyboardMarkup([
         ['Загадывай!', 'Сдаюсь!', 'Помощь'],
    ], resize_keyboard=True)


def greet_user(update, context):
    print('вызван start')
    pprint(context)
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

    elif len(str(message)) < 4:
        return 'too short string'

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


def make_number():
    while True:
        number = ''.join([str(randint(0, 9)) for i in range(4)])
        if (len(set(number)) == len(number)) and (int(number) > 999):
            return number


def send_text(update, context):

    message = update.message.text

    chat_id = update.effective_chat.id
    print(f'{chat_id} вызван send text: {message}')

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
        if context.user_data.get('number', 0):
            reply = f'Ты сдался на {context.user_data.get("turns", 0)} попытке.\n' \
                    f'Было загадано число {context.user_data["number"]}'
            # тут нужно записать попытку в DB
            # получить данные которые писать
            # проверить а нет ли такого уже в базе
            # если есть записать в turn + 1
            # если нет создать пользователя
            # давай пока без проверок просто записываем.
            context.user_data.clear()
            # if update_user_score(update, context):
            #     context.user_data.clear()
            # else:
            #     raise ValueError('something wrong!')
        else:
            reply = choice(['Не сдавайся!', 'Never give in!', 'Всё в ваших руках, поэтому не стоит их опускать'])

        update.message.reply_text(reply, reply_markup=main_keyboard())

    else:
        number = context.user_data.get('number', make_number())
        context.user_data['turns'] = context.user_data.setdefault('turns', 0) + 1
        reply = check_number_v2(message, number)

        print(f'Чат: {chat_id}, попытка {context.user_data["turns"]}')

        if reply == 'wrong input':
            update.message.reply_text('Wrong input: need 4 digits, but symbols were given.')

        elif reply == 'win':
            update.message.reply_text(f'Ты победил в {context.user_data["turns"]} попыток', reply_markup=main_keyboard())
            context.user_data.clear()
            # тут будем записывать в базу никнэйм и количество turn

        elif reply == 'too long string':
            update.message.reply_text('Too long string. Need 4 digits.')

        elif reply == 'too short string':
            update.message.reply_text('Too short string. Need 4 digits.')

        elif isinstance(reply, dict):
            # context.user_data['last_user_turn'] = message
            # context.user_data['last_bulls_cows'] = reply
            reply_message = f'Bulls {reply["bulls"]}, Cows {reply["cows"]}'
            update.message.reply_text(reply_message, reply_markup=main_keyboard())

        else:
            update.message.reply_text('something goes wrong! Please screenshot to @Rom762', reply_markup=main_keyboard())


def update_user_score(update, context):
    # id, first_name, last_name, nickname, email, games, best_turns):
    try:
        user = MyUser(first_name='William', last_name='Clinton', nickname='@willy', email='bill.clinton@usa.gov', games=1, best_turns=context.user_data['turns'])
        user.add_user()
        return True
    except Exception as exp:
        print(exp)
        return False


def main():
    bot = Updater(token=TOKEN, use_context=True)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Помощь)$'), help_user))
    dp.add_handler(MessageHandler(Filters.text, send_text))

    logging.info(f'бот стартовал {datetime.datetime.now()}')
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()





