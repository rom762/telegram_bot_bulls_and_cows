import config
import datetime
import logging
from random import choice, randint
from telegram import ReplyKeyboardMarkup, Chat
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

TOKEN = config.TOKEN

log = logging.getLogger(__name__)


def configure_logging():
    """
    configure logger
    :return:
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler("bot.log", encoding='UTF-8')
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


def main_keyboard():
    """
    generate inline-keybord
    :return: keyboard
    """
    return ReplyKeyboardMarkup([
         ['Загадывай!', 'Сдаюсь!', 'Подскажи!', 'Об игре'],
    ], resize_keyboard=True)


def greet_user(update, context):
    log.info('вызван start')
    update.message.reply_text(f'Привет, давай сыграем в игру  {config.RULES_URL}', reply_markup=main_keyboard())


def help_user():
    log.info('вызван help')

    reply = (f'Bulls это количество цифр в твоем ответе, которое ты поставил на правильное место.\n\n'
              f'Cows это количество цифр в твоем ответе, которые есть в загаданном числе, но ты их поставил не на то место\n\n'
              f'Например, загадано число 1234\n'
              f'Мы пишем боту 2574\n\n'
              f'2 - есть в загаданном числе 1234, но она стоит не на первом месте, а на втором. Значит она будет считаться в Cows\n'
              f'5 и 7 нет в загаданном числе - они не считаются\n\n'
              f'А вот 4 есть и мы поставили ее на правильное место\n'
              f'Она будет засчитана в Bulls\n\n'
              f'Ответ бота будет: Bulls: 1, Cows 1\n')

    return reply


def check_number_v2(update, context):
    message = update.message.text
    number = context.user_data.setdefault('number', make_number(context=context))
    bulls_cows = {'bulls': 0, 'cows': 0}

    if len(str(message)) > 4:
        return 'Too long string. Need 4 digits.'

    elif len(str(message)) < 4:
        return 'Too short string. Need 4 digits.'

    elif not str(message).isnumeric():
        return 'Wrong input: need 4 digits, but symbols were given.'

    elif int(message) == int(number):
        reply = f'Ты победил в {context.user_data["turns"]} попыток'
        context.user_data.clear()
        return reply

    else:
        for order, digit in enumerate(message):
            if digit in number:
                if number[order] == digit:
                    bulls_cows['bulls'] += 1
                else:
                    bulls_cows['cows'] += 1
        return f'Bulls {bulls_cows["bulls"]}, Cows {bulls_cows["cows"]}'


def make_number(context):

    if not context.user_data.get('number', 0):
        while True:
            number = ''.join([str(randint(0, 9)) for i in range(4)])
            if (len(set(number)) == len(number)) and (int(number) > 999):
                log.info(f'made right number: {number}')
                context.user_data['number'] = number
                break
            else:
                log.info(f'made wrong number: {number}')
    return context.user_data.get('number')


def send_text(update, context):

    message = update.message.text
    chat_id = update.effective_chat.id

    log.info(f'{chat_id} вызван send text: {message}')
    for key, value in context.user_data.items():
        log.debug(f'{key}: {value}')

    number = make_number(context)
    turns = context.user_data.setdefault('turns', 0)
    helps = context.user_data.setdefault('helps', 0)

    if message == 'Загадывай!':
        log.info(f'Чат {chat_id}, Загадано {number}')
        reply = 'Загадано, угадывай!'

    elif message == 'Сдаюсь!':
        if turns > 0:
            reply = f'Ты сдался на {turns} попытке.\n' \
                    f'Было загадано число {number}'
            context.user_data.clear()
        else:
            reply = choice(['Не сдавайся!', 'Never give in!', 'Всё в ваших руках, поэтому не стоит их опускать'])

    elif message == 'Подскажи!':
        reply = check_helps(context, number, helps, turns)

    elif message == 'Об игре':
        reply = help_user()

    else:
        log.info(f'Чат: {chat_id}, попытка {turns}: {message}')
        context.user_data['turns'] += 1
        reply = check_number_v2(update, context)

    update.message.reply_text(reply, reply_markup=main_keyboard())


def check_helps(context, number, helps, turns):
    if helps < 3:
        context.user_data['helps'] += 1
        hint = str(number)[helps]
        log.info(f'current hint is: {hint}')
        reply = f'На {context.user_data["helps"]} месте стоит цифра {hint}'

    else:
        reply = f'На последнем месте стоит цифра {str(number)[-1]}\n' \
                f'Ну ок. Ты победил. C 4 подсказками за {turns} попыток.\n' \
                f'Было загадано: {number}'
        context.user_data.clear()
    return reply


def main():
    bot = Updater(token=TOKEN, use_context=True)
    dp = bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('help', help_user))
    dp.add_handler(MessageHandler(Filters.regex('^(Помощь)$'), help_user))
    dp.add_handler(MessageHandler(Filters.text, send_text))

    log.info(f'бот стартовал {datetime.datetime.now()}')
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    configure_logging()
    main()





