from random import randint

number = ''
_helps = 0
_turns = 0


def make_number(silence=0):
    global number
    if NUMBER == '':
        NUMBER = str(randint(1000, 10000))

        if silence:
            return
    #print(number)
    return NUMBER

def get_turns():
    return _turns

def check_number(user_number):
    global _helps
    global _turns
    _turns += 1
    bulls = 0
    cows = 0

    if user_number == number:
        return tuple(['win', _turns])

    if user_number == 'help':
        _helps += 1
        return tuple(['help', number[_helps - 1]])

    if int(user_number) < 1000 or int(user_number) > 9999:
        return tuple(['wrong', _turns])

    for order, digit in enumerate(user_number):
        if digit in number:
            if number[order] == digit:
                bulls += 1
            else:
                cows += 1

    return tuple([bulls, cows])

if __name__ == '__main__':
    pass
else:
    make_number()