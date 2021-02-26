import logging
from pprint import pprint
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
import config
from mastermind_engine import check_number, get_turns, make_number

logging.basicConfig(filename='bot.log', level=logging.INFO)
TOKEN = config.TOKEN


def main_keyboard():
    return ReplyKeyboardMarkup([
         ['Загадывай!', 'Покажи котика'],
    #     ['Курс доллара', 'Что с погодой'],
    #     # [KeyboardButton('Мои координаты', request_location=True), KeyboardButton('Мои контакты', request_contact=True)]
    ])


def greet_user(update, context):
    print('вызван start')
    update.message.reply_text(f'Привет, давай сыграем в игру  {config.RULES_URL}', reply_markup=main_keyboard())


def guess_number(update, context):
    pass


def check_number_v2(message, number):
    bulls = 0
    cows = 0

    if len(str(message)) > 4:
        return f'too long string'

    elif not str(message).isnumeric():
        return 'wrong input'

    elif int(message) == int(number):
        return f'win'

    else:
        for order, digit in enumerate(message):
            if digit in number:
                if number[order] == digit:
                    bulls += 1
                else:
                    cows += 1
        return (bulls, cows)


def send_text(update, context):
    print('вызван send text')
    message = update.message.text
    chat_id = update.effective_chat.id

    if message == 'Загадывай!':
        if context.user_data.get('number', 0):
            update.message.reply_text(f'Для тебя уже загадано раньше {context.user_data["number"]}')
        else:
            number = make_number()
            context.user_data['number'] = number
            context.user_data['turns'] = 0
            print(f'Чат {chat_id}, Загадано {number}')
            update.message.reply_text('Загадано, угадывай!')
    else:
        number = context.user_data.get('number', make_number())
        reply = check_number_v2(message, number)
        context.user_data['turns'] += 1
        current_turns = context.user_data['turns']
        if reply == 'wrong input':
            update.message.reply_text(reply)
        elif reply == 'win':
            context.user_data['number'] = make_number()
            context.user_data['turns'] = 0
            context.user_data['last_user_turn'] = ''
            context.user_date['last_bulls_cows'] = ()
            update.message.reply_text(f'Ты победил в {current_turns} попыток')
        elif reply == 'too long string':
            update.message.reply_text(reply)
        elif isinstance(reply, tuple):
            context.user_data['last_user_turn'] = message
            context.user_data['last_bulls_cows'] = reply
            reply_message = f'Bulls {reply[0]}, Cows {reply[1]}'
            update.message.reply_text(reply_message)
        else:
            update.message.reply_text('something goes wrong!')


def main():
    my_bot = Updater(token=TOKEN, use_context=True)
    dp = my_bot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('guess', guess_number))

    dp.add_handler(MessageHandler(Filters.text, send_text))
    logging.info('бот стартовал')
    my_bot.start_polling()
    my_bot.idle()


# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
#     bot.reply_to(message, "Howdy, how are you doing?")
#     pprint(message)
#
# @bot.message_handler(func=lambda m: True)
# def start(message):
#     user_text = message.text
#     chat_id = message.chat.id
#     #print(begin_text, type(begin_text), message.chat.id)
#     print('=====================================')
#
#     answer = list(check_number(user_text, chat_id))
#     if str(answer[0]) == 'wrong':
#         bot_message = 'Wrong number'
#
#     elif str(answer[0]) == 'win':
#         bot_message = 'You win!'
#
#     elif str(answer[0]) == 'help':
#         bot_message = f'Help: {answer[1]}'
#     else:
#         bot_message = f'bulls: {answer[0]}, cows: {answer[1]}'
#
#     print(f'Шаг: {get_turns()}, Чат: {message.chat.id}, Сообщение: {message.text}')

    # bot.reply_to(message, bot_message)

if __name__ == '__main__':
    main()





