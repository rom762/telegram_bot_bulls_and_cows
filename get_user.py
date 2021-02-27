from models import User
from database import db_session

user = User.query.first()
print(f"""
Name: {user.name}
Salary: {user.salary}
E-mail: {user.email}
""")