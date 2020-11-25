from pprint import pprint
from random import randint

mydata = {}



chat_ids = ['test', 'test2', 'test3', 'test4', 'test']

# for chat_id in chat_ids:
#     mydata.setdefault(chat_id, dict())
#     mydata[chat_id].setdefault('helps', 0)
#     mydata[chat_id].setdefault('turns', 0)
#     mydata[chat_id].setdefault('number', randint(1000, 10000))
#     print(chat_id, mydata[chat_id])


# user_message = ['test', 'help', 'win', 1234, '1234']
#
# for each in user_message:
#     if str(each) == 'help':
#         print(f'{each} valid')
#     elif not str(each).isnumeric():
#         print(f'{str(each)} not valid')
#     elif 1000 < int(str(each)) < 1000:
#         print(f'{str(each)} valid')
#     else:
#         print(f'{str(each)} not valid')

#pprint(mydata)

for i in range(10):
    number = ''.join([str(randint(0, 9)) for i in range(4)])
    print(i, number)