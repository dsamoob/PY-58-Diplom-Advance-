import sqlalchemy
from sqlalchemy.orm import sessionmaker
import config as config
from DB.db_models import Match, User, FavoriteList, UnFavoriteList, SearchingList
from DB.class_DBapp import DBapp
import psycopg2


conn = psycopg2.connect(database=config.db_name, user=config.db_login, password=config.db_password)
DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
dbapp = DBapp(User, Match, FavoriteList, UnFavoriteList, SearchingList, session, conn)
path = '/Users/egorbelov/GitHub/PY-58-Diplom-Advance/VK/total.json'


if __name__ == '__main__':
    # create_tables(engine)
    # [dbapp.add_user(i) for i in data.users]
    dbapp.add_to_searching_list(path)
    print(dbapp.get_previous_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())
    print(dbapp.get_previous_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())
    print(dbapp.get_next_search())





