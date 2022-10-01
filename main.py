import config
import psycopg2
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from vk_api.longpoll import VkEventType
from DB.class_DBapp import DBapp
from DB.db_models import create_tables, Match, User, FavoriteList, UnFavoriteList, SearchingList
from VK.class_VKapp import VKapp
from VK.keyboard import send_kb, send_kb_in_message

conn = psycopg2.connect(database=config.db_name, user=config.db_login, password=config.db_password)
DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
dbapp = DBapp(User, Match, FavoriteList, UnFavoriteList, SearchingList, session, conn)
vkapp = VKapp(token_user=config.vk_token_prog, tokenVK_Group=config.vk_token_my)
path = 'total.json'


if __name__ == '__main__':

    create_tables(engine)
    for event in vkapp.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                send_kb(user_id, msg.lower())
                if msg == 'hi':
                    vkapp.send_msg(user_id, 'hello friend')
                    vkapp.send_msg(user_id, 'how a u?')
                elif msg == 'ok':
                    vkapp.send_msg(user_id, 'tell the amoun of 5 and 5)')
                    vkapp.send_msg(user_id, user_id)
                elif msg == 'name':
                    vkapp.send_msg(user_id, vkapp.get_name(user_id))
                elif msg == 'adge':
                    vkapp.send_msg(user_id, vkapp.get_age(user_id))
                elif msg == 'city':
                    vkapp.send_msg(user_id, vkapp.get_id_city(user_id))
                elif msg == 'sex':
                    vkapp.send_msg(user_id, vkapp.get_reverse_sex(user_id))
                elif msg == 'search':
                    vkapp.create_file(vkapp.total_dict(user_id))
                    dbapp.add_to_searching_list(path)
                    result = dbapp.get_next_search()
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    send_kb_in_message(user_id, msg.lower(), result[0])
                    vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                    result = dbapp.get_next_search()
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    send_kb_in_message(user_id, msg.lower(), result[0])
                    vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                    result = dbapp.get_next_search()
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    send_kb_in_message(user_id, msg.lower(), result[0])
                    vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                elif msg.split('_')[0] == 'black':
                    # код для вставки анкеты с ID {msg.split('_')[1]} в чёрный список
                    print(f"BLACK ID {msg.split('_')[1]}")
                elif msg.split('_')[0] == 'favorite':
                    # код для вставки анкеты с ID {msg.split('_')[1]} в избранное
                    print(f"Favorite ID {msg.split('_')[1]}")
                elif msg == "<back":
                    pass #переход к предыдущим анкетам
                elif msg == 'next>':
                    pass # сл анкеты
                elif msg == 'view_favorite':
                    pass # показать избранное
                elif msg == 'view_black':
                    pass # Показать черный список

