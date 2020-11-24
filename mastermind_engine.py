from random import randint

NUMBER = ''
_helps = 0
_turns = 0


def make_number(silence=0):
    while True:
        number = str(randint(1000, 10000))
        if len(set(number)) == len(number):
            return number


def get_turns():
    return _turns

def check_number(user_number):
    global _helps
    global _turns
    global NUMBER
    _turns += 1
    bulls = 0
    cows = 0

    if user_number == NUMBER:
        return tuple(['win', _turns])

    if user_number == 'help':
        _helps += 1
        return tuple(['help', NUMBER[_helps - 1]])

    if int(user_number) < 1000 or int(user_number) > 9999:
        return tuple(['wrong', _turns])

    for order, digit in enumerate(user_number):
        if digit in NUMBER:
            if NUMBER[order] == digit:
                bulls += 1
            else:
                cows += 1

    return tuple([bulls, cows])

if __name__ == '__main__':
    pass
else:
    NUMBER = make_number()
    print(f'ЗАГАДАНО: {NUMBER}')