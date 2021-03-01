from pprint import pprint
from random import randint

NUMBER = ''
_helps = 0
_turns = 0
data = {
    #chat_id {'helps': 0, 'turns' : 0, numer=''}
}


def get_turns():
    return _turns


def check_number(user_message, chat_id):
    bulls = 0
    cows = 0
    data.setdefault(chat_id, dict())
    data[chat_id]['helps'] = data[chat_id].setdefault('helps', 0)
    data[chat_id]['turns'] = data[chat_id].setdefault('turns', -1) + 1
    number = data[chat_id].setdefault('number', make_number())
    pprint(data)

    if user_message == number:
        # если угадал загадываем новое число
        data[chat_id]['number'] = make_number()
        return tuple(['win', _turns])

    if user_message == 'help':
        if data[chat_id]['helps'] < 4:
            data[chat_id]['helps'] += 1
            return tuple(['help', number[data[chat_id]['helps'] - 1]])
        else:
            data[chat_id]['number'] = make_number()
            return tuple(['win', _turns])

    if not str(user_message).isnumeric():
        return tuple(['wrong', _turns])

    if len(str(user_message)) < 4:
        return tuple(['wrong', _turns])

    if int(user_message) < 1000 or int(user_message) > 9999:
        return tuple(['wrong', _turns])

    for order, digit in enumerate(user_message):
        if digit in number:
            if number[order] == digit:
                bulls += 1
            else:
                cows += 1

    return tuple([bulls, cows])


if __name__ == '__main__':

    while True:

        chat_id = 'test' + str(randint(1, 6))
        user_text = input(f'{chat_id}, Введите число: ')
        answer = list(check_number(user_text, chat_id))
        if str(answer[0]) == 'wrong':
            print('Wrong number')

        elif str(answer[0]) == 'win':
            print('You win!')

        elif str(answer[0]) == 'help':
            print(f'Help: {answer[1]}')
        else:
            print(f'bulls: {answer[0]}, cows: {answer[1]}')

        print(f'Шаг: {data[chat_id]["turns"]}, Чат: {chat_id}, Сообщение: {user_text}')





