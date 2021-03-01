from pprint import pprint

from models import MyUser
from database import db_session, engine

user = MyUser.query.first()
print(type(user))
print(user)

# name = input('Firstname: ').strip().capitalize()

result = db_session.execute(f'SELECT * FROM users WHERE users.first_name == Mark')
print(*result)

