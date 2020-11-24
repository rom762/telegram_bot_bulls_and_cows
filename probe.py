from random import randint

number = ''

def make_number(silence=0):
    while True:
        number = str(randint(1000, 10000))
        print(number)

        if len(set(number)) == len(number):
            return number


make_number()


