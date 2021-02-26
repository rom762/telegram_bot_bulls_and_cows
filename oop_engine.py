from random import randint


class Game:

    games = 0

    def __init__(self, chat_id):

        Game.games += 1
        self.chat = chat_id
        self._helps = 0
        self._turns = 0
        while True:
            number = str(randint(1000, 10000))
            if len(set(number)) == len(number):
                self.__number = number
                break

    def get_number(self):
        return self.__number

    def check_number(self, user_number):

        if user_number == self.__number:
            #тут надо убивать экземпляр класса
            del self.__number
            return tuple(['win', self._turns])

        if user_number == 'help':
            self._helps += 1
            return tuple(['help', self.__number[self._helps - 1]])

        if int(user_number) < 1000 or int(user_number) > 9999:
            return tuple(['wrong', self._turns])

        for order, digit in enumerate(user_number):
            if digit in self.__number:
                if self.__number[order] == digit:
                    bulls += 1
                else:
                    cows += 1

        return tuple([bulls, cows])

    # def __del__(self):


if __name__ == '__main__':
    chat1 = '12345'
    chat2 = '12346'
    chat3 = '12347'

    user1 = Game(chat1)
    user2 = Game(chat2)
    user3 = Game(chat3)

    print(Game.games)

    for each in Game():
        print(each.get_number())
    # print(user1.get_number())
    # print(user2.get_number())




