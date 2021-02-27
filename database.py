from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://lrdxfjnh:gcb0qqm_x-K7mxF0Zo2BCM7DUhmXjwfE@rogue.db.elephantsql.com:5432/lrdxfjnh')
db_session = scoped_session(sessionmaker(bind=engine))

# эта часть не обязательна, но она добавляет удобства и позволяет работать из нашей модели с БД
Base = declarative_base()
Base.query = db_session.query_property()

