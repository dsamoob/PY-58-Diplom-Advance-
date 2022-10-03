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
    # create_tables(engine)
    # for i in data.match:
    #     dbapp.add_match(i)
    # for i in data.users:
    #     dbapp.add_user(i)
    # dbapp.get_user_pk('781002')
    # dbapp.add_user(9681602)
    # dbapp.add_match(470680882)
    # dbapp.add_match_to_favorite(9681602, 470680882)
    dbapp









