from database import db_session
from models import User

user = User(name='July', salary=2000_000, email='july.nika@ya.ru', telegram_id=2)
db_session.add(user)
db_session.commit()