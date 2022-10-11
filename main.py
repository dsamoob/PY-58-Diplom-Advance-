import config as config
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from vk_api.longpoll import VkEventType
from DB.class_DBapp import DBapp
from DB.db_models import create_tables
from VK.class_VKapp import VKapp
import time

command_list = ['name', 'adge', 'city', 'sex', 'начали', 'сдедующая', 'предыдущая', 'предыдущая', 'в черный список',
                'в избранное', 'список избранного', 'черный список', 'удалить черное', 'удалить избранное']
DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

dbapp = DBapp(session)
vkapp = VKapp(token_user=config.vk_token_prog, token_vk_group=config.vk_token_my)

def messaging_next(user_id: int) -> dict:  # функция для проверки следующего (основа проверки в вк)
    result = dbapp.get_next_search(user_id)
    checking = vkapp.photo_dic(result[0])
    if checking == 0:
        time.sleep(0.3)
        return messaging_next(user_id)
    time.sleep(0.3)
    return result


def messaging_previous(user_id: int) -> dict:  # функция для проверки предыдущего(основа проверки в вк)
    result = dbapp.get_previous_search(user_id)
    checking = vkapp.photo_dic(result[0])
    if checking == 0:
        time.sleep(0.3)
        return messaging_previous(user_id)
    time.sleep(0.3)
    return result


if __name__ == '__main__':
    for event in vkapp.longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                msg = event.text.lower()
                user_id = event.user_id  # определние ид пользователя
                if msg in ['начали', 'обновить']:
                    dbapp.add_to_searching_list(vkapp.total_dict(user_id), user_id)  # заполнения поисквого списка для пользователя
                    dbapp.set_user_log(user_id)  # заполняет лог для пользователя
                    result = dbapp.get_first_search(user_id)  # выдает первое совпадения для пользователя не меняя лог
                    vkapp.message_after(user_id, 'клавиатура внизу')
                    vkapp.send_msg(user_id,  # выдает первый результат согласно логам пользователя
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_photo(user_id, result[0])
                elif msg == 'следующая':
                    result = messaging_next(user_id)
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_photo(user_id, result[0])
                elif msg == 'предыдущая':
                    result = messaging_previous(user_id)
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_photo(user_id, result[0])
                elif msg == 'в черный список':  # при добавлении найденного в список - добавляет и переводит к следующей анкете
                    match_id = dbapp.get_match_id_by_id(dbapp.get_actual_index(user_id))
                    dbapp.add_match(match_id)  # добавляет в табилцу используемых найденышей
                    dbapp.add_match_to_unfavorite(user_id, match_id)  # добавляет в сам список
                    result = messaging_next(user_id)
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_photo(user_id, result[0])
                elif msg == 'в избранное':  # при добавлении найденного в список - добавляет и переводит к следующей анкете
                    match_id = dbapp.get_match_id_by_id(dbapp.get_actual_index(user_id))
                    dbapp.add_match(match_id)  # добавляет в табилцу используемых найденышей
                    dbapp.add_match_to_favorite(user_id, match_id)   # добавляет в сам список
                    result = messaging_next(user_id)
                    vkapp.send_msg(user_id,
                                   f'{result[1]} {result[2]}\n'
                                   f'https://vk.com/id{result[0]}\n'
                                   )
                    vkapp.send_photo(user_id, result[0])
                elif msg == 'список избранного':
                    result = dbapp.get_favorite_list(user_id)  # получение списка
                    if result == 0:  # если списка нет
                        vkapp.send_msg(user_id, f'список пуст')
                    else:
                        for item in result:  # в цикле проходится по списку если он есть
                            vkapp.message_del_favorite(user_id, f'{item[1]} {item[2]}\n'  # в сообщении есть кнопка на удаление
                                                                f'https://vk.com/id{item[0]}\n', item[0])
                elif msg == 'черный список':
                    result = dbapp.get_unfavorite_list(user_id)   # получение списка
                    if result == 0: # если списка нет
                        vkapp.send_msg(user_id, f'список пуст')
                    else:
                        for item in result:  # в цикле проходится по списку
                            vkapp.message_del_unfavorite(user_id, f'{item[1]} {item[2]}\n'  # в сообщении есть кнопка на удаление
                                                                  f'https://vk.com/id{item[0]}\n', item[0])
                elif msg.split('_')[0] == 'удалить черное':
                    dbapp.del_from_unfavorite(user_id, msg.split('_')[1])
                    vkapp.send_msg(user_id, f"{msg.split('_')[1]} удален из черного списка")

                elif msg.split('_')[0] == 'удалить избранное':
                    dbapp.del_from_favorite(user_id, msg.split('_')[1])
                    vkapp.send_msg(user_id, f"{msg.split('_')[1]} удален из списка избранных списка")

                elif msg not in command_list:  # любое входящее сообщение, что не в список команд
                    result = dbapp.add_user(user_id)  # добавление/нахождение пользователя в бд
                    if result == 1:  # если пользователь заходит первый раз
                        vkapp.start(user_id, f'Привет {vkapp.get_name(user_id)}, ждми кнопку для начала!')
                    if result == 0:  # если пользователь ранее обращался к приложению он уже есть в бд
                        vkapp.message_after(user_id, f'Привет {vkapp.get_name(user_id)}, давай продолжим!\n'
                                                     f'клавиатура внизу')

