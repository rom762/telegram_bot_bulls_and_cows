from database import db_session
from models import User


# внимакние тут first не значит first Он просто отдает рандомного usera
user = User.query.first()

db_session.delete(user)
db_session.commit()