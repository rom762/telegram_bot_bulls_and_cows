import sqlalchemy
import psycopg2
import pymysql


conn = 'mysql+mysqldb://:test@dsstudents.skillbox.ru:5432/db_ds_students'

engine = sqlalchemy.create_engine("mysql[+pymysql]://roman:password@localhost/bullscows")
                                  # dialect[+driver]://user:password@host/dbname[?key=value..]
connect = engine.connect()
inspector = sqlalchemy.inspect(engine)
print(inspector.get_table_names())

ds