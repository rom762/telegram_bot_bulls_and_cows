from database import db_session
from models import User


user = User.query.first()

user.salary = 1999_999
db_session.commit()