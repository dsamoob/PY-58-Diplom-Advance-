import config as config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from vk_api.longpoll import VkEventType
from DB.class_DBapp import DBapp
from DB.db_models import create_tables
from VK.class_VKapp import VKapp

DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

dbapp = DBapp(session)
vkapp = VKapp(token_user=config.vk_token_prog, token_vk_group=config.vk_token_my)

if __name__ == '__main__':
    create_tables(engine)
    for event in vkapp.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id
                dbapp.add_user(user_id)
                if msg in ['hi', 'hello', 'good day', 'привет', 'хай']:
                    vkapp.start(user_id, 'приветики, нажми кнопку!')
                elif msg == 'name':
                    vkapp.send_msg(user_id, vkapp.get_name(user_id))
                elif msg == 'adge':
                    vkapp.send_msg(user_id, vkapp.get_age(user_id))
                elif msg == 'city':
                    vkapp.send_msg(user_id, vkapp.get_id_city(user_id))
                elif msg == 'sex':
                    vkapp.send_msg(user_id, vkapp.get_reverse_sex(user_id))
                elif msg == 'начали':
                    dbapp.add_to_searching_list(vkapp.total_dict(user_id), user_id)
                    dbapp.set_user_log(user_id)
                    result = dbapp.get_first_search(user_id)
                    vkapp.message_after(user_id, 'клавиатура внизу')
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                elif msg == 'следующая':
                    result = dbapp.get_next_search(user_id)
                    if result != 0:
                        vkapp.send_msg(user_id,
                                       f'{result[1]} {result[2]}\n'
                                       f'https://vk.com/id{result[0]}\n'
                                       )
                        vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                    else:
                        vkapp.send_msg(user_id, f'конец списка')
                elif msg == 'предыдущая':
                    result = dbapp.get_previous_search(user_id)
                    if result != 0:
                        vkapp.send_msg(user_id,
                                       f'{result[1]} {result[2]}\n'
                                       f'https://vk.com/id{result[0]}\n'
                                       )
                        vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                    else:
                        vkapp.send_msg(user_id, f'до ничего, только следующая')
                elif msg == 'в черный список':
                    match_id = dbapp.get_match_id_by_id(dbapp.get_actual_index(user_id))
                    dbapp.add_match(match_id)
                    dbapp.add_match_to_unfavorite(user_id, match_id)
                    result = dbapp.get_next_search(user_id)
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                elif msg == 'в избранное':
                    match_id = dbapp.get_match_id_by_id(dbapp.get_actual_index(user_id))
                    dbapp.add_match(match_id)
                    dbapp.add_match_to_favorite(user_id, match_id)
                    result = dbapp.get_next_search(user_id)
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_foto(user_id=user_id, user_id_foto=result[0])
                elif msg == 'список избранного':
                    for item in dbapp.get_favorite_list(user_id):
                        vkapp.message_del_favorite(user_id, f'{item[1]} {item[2]}\n'
                                                            f'https://vk.com/id{item[0]}\n', item[0])
                elif msg == 'черный список':
                    for item in dbapp.get_unfavorite_list(user_id):
                        vkapp.message_del_unfavorite(user_id, f'{item[1]} {item[2]}\n'
                                                              f'https://vk.com/id{item[0]}\n', item[0])
                elif msg.split('_')[0] == 'удалить черное':
                    dbapp.del_from_unfavorite(user_id, msg.split('_')[1])

                elif msg.split('_')[0] == 'удалить избранное':
                    dbapp.del_from_favorite(user_id, msg.split('_')[1])
