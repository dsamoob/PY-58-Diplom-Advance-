import sqlalchemy
from sqlalchemy.orm import sessionmaker
from DB.db_models import Match, User, FavoriteList, UnFavoriteList, SearchingList
from DB.class_DBapp import DBapp
import psycopg2
import json
from VK.class_VKapp import VK
from vk_api.longpoll import VkEventType
import config

conn = psycopg2.connect(database=config.db_name, user=config.db_login, password=config.db_password)
DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()
dbapp = DBapp(User, Match, FavoriteList, UnFavoriteList, SearchingList, session, conn)
path = 'total.json'

if __name__ == '__main__':
    bot = VKapp(token_user=config.vk_token_prog, tokenVK_Group=config.vk_token_my)


    def create_file(total_dict):
        with open(f"total.json", "w", encoding='UTF-8') as write_file:
            json.dump(total_dict, write_file)
        print(f'Создан файл: total.json')
    for event in bot.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                # sended_keybord(user_id, msg.lower())
                if msg == 'hi':
                    bot.send_msg(user_id, 'hellow froend')
                    bot.send_msg(user_id, 'how a u?')
                if msg == 'ok':
                    bot.send_msg(user_id, 'tell the amoun of 5 and 5)')
                    bot.send_msg(user_id, user_id)
                if msg == 'name':
                    bot.send_msg(user_id, bot.get_name(user_id))
                if msg == 'adge':
                    bot.send_msg(user_id, bot.get_age(user_id))
                if msg == 'city':
                    bot.send_msg(user_id, bot.get_id_city(user_id))
                if msg == 'sex':
                    bot.send_msg(user_id, bot.get_reverse_sex(user_id))
                if msg == 'search':
                    total_dict = bot.total_dict(user_id)
                    create_file(total_dict)
                    dbapp.add_to_searching_list(path)
                    result = dbapp.get_next_search()
                    bot.send_msg(user_id,
                                f'{result[1]} {result[2]}\n'
                                f'https://vk.com/id{result[0]}\n'
                                f'место для фото1\n'
                                f'место для фото2\n'
                                f'место для фото3'
                                 )
                    result = dbapp.get_next_search()
                    bot.send_msg(user_id,
                                 f'{result[1]} {result[2]}\n'
                                 f'https://vk.com/id{result[0]}\n'
                                 f'место для фото1\n'
                                 f'место для фото2\n'
                                 f'место для фото3'
                                 )
                    result = dbapp.get_next_search()
                    bot.send_msg(user_id,
                                 f'{result[1]} {result[2]}\n'
                                 f'https://vk.com/id{result[0]}\n'
                                 f'место для фото1\n'
                                 f'место для фото2\n'
                                 f'место для фото3'
                                 )

