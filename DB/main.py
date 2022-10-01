import sqlalchemy
from sqlalchemy.orm import sessionmaker
import config as config
from DB.db_models import create_tables, Match, User, FavoriteList, UnFavoriteList, SearchingList
from DB.class_DBapp import DBapp
import psycopg2
import data


conn = psycopg2.connect(database=config.db_name, user=config.db_login, password=config.db_password)
DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
dbapp = DBapp(User, Match, FavoriteList, UnFavoriteList, SearchingList, session)
path = '/Users/egorbelov/GitHub/PY-58-Diplom-Advance/VK/total.json'


if __name__ == '__main__':
    # create_tables()
    # for i in data.match:
    #     dbapp.add_match(i)
    # for i in data.users:
    #     dbapp.add_user(i)
    # dbapp.get_user_pk('781002')
    # dbapp.get_user_pk('12')
    # dbapp.get_match_pk('00124002')
    # # create_tables(engine)
    # dbapp.add_match('12345')
    # dbapp.add_match('0000')
    # dbapp.add_match('00002')
    # dbapp.add_match('0000')
    # dbapp.add_match('00124002')
    # dbapp.add_match('00124002')
    dbapp.test('483857710')







