from sqlalchemy import Column, Integer, String, IdentityOptions
from database import Base, engine, db_session


class MyUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String())
    last_name = Column(String())
    nickname = Column(String()) # тут наверное надо хранить телеграм ник
    games = Column(Integer())
    best_turns = Column(Integer) # пока будем просто хранить во сколько ходов выиграл
    email = Column(String(120), unique=True)
    # telegram_id = Column(Integer(), unique=True)

    def __repr__(self):
        return f"""Firstname: {self.first_name},
                   Lastname: {self.last_name},
                   games: {self.games},
                   best turn: {self.best_turns}, 
                   """

    def __init__(self, id, first_name, last_name, nickname, email, games, best_turns=100):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.email = email
        self.games = games
        self.best_turns = best_turns

    def delete_user(self):
        db_session.delete(self)
        db_session.commit()

    def add_user(self):
        db_session.add(self)
        db_session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String())
#     lastname = Column(String())
#     salary = Column(Integer())
#     email = Column(String(120), unique=True)
#     telegram_id = Column(Integer(), unique=True)
#
#     def __repr__(self):
#         return f'User {self.id}, {self.name}'

