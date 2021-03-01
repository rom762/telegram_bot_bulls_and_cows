from random import randint
from database import db_session
from models import MyUser


def add_user(data):
    my_user = MyUser(**data)
    print(my_user)
    return my_user
# user = User(name='Jacob', salary=randint(20000, 1000_000), email='jacob_thornton@ya.ru', telegram_id=randint(99999, 999999))
# db_session.add(user)
# db_session.commit()


fake_users = [
    {'id': 1,
        'first_name': 'Roman',
        'last_name': 'Tarkov',
        'nickname': '@Rom762',
        'games': 200,
        'best_turns': 12,
        'email': 'roman_tarkov@google.com',
     },
    {
        'id': 2,
        'first_name': 'July',
        'last_name' : 'Bordjia',
        'nickname': '@lavina',
        'games': randint(10, 200),
        'best_turns': randint(5, 20),
        'email': 'july_bor765@yahoo.com',
    },
    {
        'id': 3,
        'first_name': 'Jacob',
        'last_name' : 'Thornton',
        'nickname': '@Thor555',
        'games': randint(10,200),
        'best_turns': randint(5,20),
        'email': 'jacob_thor555@yandex.ru',
    },
    {
        'id': 4,
        'first_name': 'Mark',
        'last_name' : 'Otto',
        'nickname': '@MarkOtto123',
        'games': randint(10,200),
        'best_turns': randint(5,20),
        'email': 'ottovan_mark@google.com',
    },
    {
        'id': 5,
        'first_name': 'John',
        'last_name' : 'Week',
        'nickname': '@JohnWeek32',
        'games': randint(10, 200),
        'best_turns': randint(5,20),
        'email': 'killthemall@google.com',
    },
    {
        'id': 6,
        'first_name': 'John',
        'last_name' : 'Walker',
        'nickname': '@Walker',
        'games': randint(10, 200),
        'best_turns': randint(5,20),
        'email': 'johnny_walker@google.com',
    },
    {
        'id': 6,
        'first_name': 'John',
        'last_name' : 'Walker',
        'nickname': '@Walker',
        'games': randint(10, 200),
        'best_turns': randint(5,20),
        'email': 'johnny_walker@google.com',
    },
]


print(fake_users[5])

walker = MyUser(**fake_users[5])

# add_user(fake_users[0])
