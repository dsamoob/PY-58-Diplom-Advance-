import sqlalchemy
from sqlalchemy.orm import sessionmaker
import config as config
from DB.class_DBapp import DBapp
from data import searching_list
from DB.db_models import create_tables


DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
dbapp = DBapp(session)

"""Для теста"""
if __name__ == '__main__':
    create_tables(engine)
    user_id = 7516145
    dbapp.add_user(user_id)  # добавление пользователя
    dbapp.add_to_searching_list(searching_list, user_id)  # загрузка поискового списка по пользователю
    dbapp.add_match(551804125)   # добавление в соотвествие
    dbapp.add_match(412680665)
    dbapp.add_match(147707590)
    dbapp.add_match(380944656)
    dbapp.add_match_to_favorite(user_id, 551804125)  # добавление в список избранных
    dbapp.add_match_to_favorite(user_id, 147707590)
    dbapp.add_match_to_unfavorite(user_id, 412680665)  # добавление в черный список
    dbapp.add_match_to_unfavorite(user_id, 380944656)
    print('список избранных', dbapp.get_favorite_list(user_id))
    print('список черных', dbapp.get_unfavorite_list(user_id))
    dbapp.del_favorite(user_id, 147707590)  # удаление из списка избранных
    dbapp.del_unfavorite(user_id, 380944656)
    print('список избранных после удаления', dbapp.get_favorite_list(user_id))
    print('список черных после удаления', dbapp.get_unfavorite_list(user_id))
