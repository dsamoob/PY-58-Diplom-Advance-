from datetime import datetime
import requests
import vk_api
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import time
import json
import pprint

class VKapp:
    def __init__(self, token_user, token_vk_group, version='5.131'):
        self.token_user = token_user
        self.tokenVK_Group = token_vk_group
        self.version = version
        self.paramsVK_Group = {'access_token': self.tokenVK_Group, 'v': self.version}
        self.params_User = {'access_token': self.token_user, 'v': self.version}
        self.vk = vk_api.VkApi(token=token_vk_group)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.vk_session = vk_api.VkApi(token=token_vk_group)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ
        self.dict_cash = {}
        """стартовое меню"""
        self.key_start = VkKeyboard(one_time=True)
        self.key_start.add_button(label='Начали', color=VkKeyboardColor.PRIMARY)
        """постоянное меню"""
        self.key_fix = VkKeyboard(one_time=False)
        self.key_fix.add_button(label='Предыдущая', color=VkKeyboardColor.PRIMARY)
        self.key_fix.add_button(label='В черный список', color=VkKeyboardColor.NEGATIVE)
        self.key_fix.add_button(label='В избранное', color=VkKeyboardColor.POSITIVE)
        self.key_fix.add_button(label='Следующая', color=VkKeyboardColor.PRIMARY)
        self.key_fix.add_line()
        self.key_fix.add_button(label='Черный список', color=VkKeyboardColor.PRIMARY)
        self.key_fix.add_button(label='Обновить', color=VkKeyboardColor.POSITIVE)
        self.key_fix.add_button(label='Список избранного', color=VkKeyboardColor.PRIMARY)

    def send_msg(self, user_id, message, keyboard=None, attachment=None):
        self.vk_session.method("messages.send", {"user_id": user_id,
                                                 "message": message,
                                                 "random_id": 0,
                                                 'keyboard': keyboard,
                                                 'attachment': attachment})

    """стартовая кнопка"""
    def start(self, user_id, message):
        self.send_msg(user_id=user_id, message=message, keyboard=self.key_start.get_keyboard())
    """меню после нажатия кнопки Начали"""
    def message_after(self, user_id, message):
        self.send_msg(user_id=user_id, message=message, keyboard=self.key_fix.get_keyboard())
    """прикрепленная кнопка удаления к перечислению списка избранных"""
    def message_del_favorite(self, user_id, message, vk_id):
        key_temp = VkKeyboard(inline=True)
        key_temp.add_button(label=f'Удалить избранное_{vk_id}', color=VkKeyboardColor.NEGATIVE)
        self.send_msg(user_id=user_id, message=message, keyboard=key_temp.get_keyboard())
    """ прикрепленная кнопка удаления к перечислению черного списка"""
    def message_del_unfavorite(self, user_id, message, vk_id):
        key_temp = VkKeyboard(inline=True)
        key_temp.add_button(label=f'Удалить черное_{vk_id}', color=VkKeyboardColor.NEGATIVE)
        self.send_msg(user_id=user_id, message=message, keyboard=key_temp.get_keyboard())

    def users_info(self, user_id):
        response = self.dict_cash.get(user_id)
        if response is None:
            url = 'https://api.vk.com/method/users.get'
            params = {'user_ids': user_id, 'fields': 'city, sex, bdate, photo_id'}
            response = requests.get(url, params={**self.paramsVK_Group, **params}).json()
            self.dict_cash.clear()
            self.dict_cash[user_id] = response
        return response

    def get_name(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТ НАПИСАЛ БОТУ"""
        response = self.users_info(user_id)
        try:
            return response['response'][0]['first_name']
        except KeyError:
            self.send_msg(user_id, 'Ошибка токена')

    def get_last_name(self, user_id):
        """ПОЛУЧЕНИЕ ИМЕНИ ПОЛЬЗОВАТЕЛЯ, КОТ НАПИСАЛ БОТУ"""
        response = self.users_info(user_id)
        try:
            return response['response'][0]['last_name']
        except KeyError:
            self.send_msg(user_id, 'Ошибка токена')

    def get_age(self, user_id):
        """ПОЛУЧЕНИЕ ВОЗРАСТА"""
        response = self.users_info(user_id)
        date = response['response'][0].get('bdate')
        if (date is not None) and (len(date.split('.'))) == 3:
            year = datetime.now().year
            print(date)
            return year - datetime.strptime(date, '%d.%m.%Y').year
        else:
            self.send_msg(user_id, 'Сколько Вам лет: ')
            for event in self.longpoll.listen():
                if event.to_me:
                    age = event.text.lower()
                    try:
                        a = int(age)
                    except:
                        return 35
                    if (a > 65) or (a < 16):
                        return 35
                    else:
                        return a

    def get_primary_foto_id(self, user_id):
        """ГЛАВНАЯ ФОТОГРАФИЯ ПОЛЬЗОВАТЕЛЯ"""
        response = self.users_info(user_id)
        try:
            foto = response['response'][0]['photo_id']
            return foto.split(sep='_')[1]
        except KeyError:
            self.send_msg(user_id, 'Ошибка токена')

    def get_id_city(self, user_id):
        response = self.users_info(user_id)
        try:
            return response['response'][0]['city']['id']
        except KeyError:
            return None

    def get_reverse_sex(self, user_id):
        """ПОЛУЧЕНИЕ ИНД. ПРОТИВОПОЛ ПОЛА"""
        response = self.users_info(user_id)
        try:
            sex = response['response'][0]['sex']
        except KeyError:
            self.send_msg(user_id, 'Ошибка токена')
        if sex == 1:
            return 2
        elif sex == 2:
            return 1
        else:
            return 0

    def get_sex(self, user_id):
        """ПОЛУЧЕНИЕ ИНД. ПОЛА"""
        response = self.users_info(user_id)
        try:
            return response['response'][0]['sex']
        except KeyError:
            self.send_msg(user_id, 'Ошибка токена')

    def user_foto(self, user_id, album='profile', offset=0):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': user_id, 'album_id': album, 'extended': '1', 'photo_sizes': '1', 'offset': offset}
        response = requests.get(url, params={**self.params_User, **params})
        time.sleep(0.3)
        return response.json()

    def foto_dict(self, user_id, list_album='profile'):  # словарь вида {like:owenID_fotoID}
        dict_foto = {}
        print(f'Ищем фото{user_id}')
        album = list_album
        # for album in list_album:  # альбомы на стене и в профайле
        offset = 0
        total = (self.user_foto(user_id, album))['response']['count']
        while True:
            user_foto = self.user_foto(user_id, album, offset)
            for item in (user_foto['response']['items']):  # заходим в гр. фотографий
                like = item['likes']['count']
                post_id = item['id']
                max_size = 0
                dict_foto[like] = f"{user_id}_{item['id']}"
            offset += len(user_foto['response']['items'])
            if offset >= user_foto['response']['count']:
                break
        sort_key = sorted(dict_foto, reverse=True)
        sort_dict = {x: dict_foto[x] for x in sort_key}
        while len(sort_dict) > 3:
            sort_dict.popitem()
        return sort_dict

    def total_dict(self, user_id):
        tot_dict = {}
        response = self.search_user(user_id)
        if response.get('response') is not None:
            print(len(response['response']['items']))
            for serch_user in response['response']['items']:
                if (serch_user['is_closed'] == False) and (serch_user.get('bdate') is not None):
                    if len(serch_user.get('bdate').split('.')) > 2:
                        city_title = None
                        if serch_user.get('city') is not None:
                            city_title = serch_user['city']['title']
                        tot_dict[serch_user['id']] = {
                            'first_name': serch_user['first_name'],
                            'last_name': serch_user['last_name'],
                            'sex': serch_user['sex'],
                            'age': datetime.now().year - datetime.strptime(serch_user['bdate'], '%d.%m.%Y').year,
                            'city': city_title
                        }
            print(len(tot_dict))
            return tot_dict

    def search_user(self, user_id, down_age=1, up_age=1, count=1000):  # Вывод найденных пользователе
        """ПОИСК ПОЛЬЗОВАТЕЛЯ ПО ДАННЫМ"""
        age = self.get_age(user_id)
        url = f'https://api.vk.com/method/users.search'
        params = {
            'sex': self.get_reverse_sex(user_id),
            'age_from': age - down_age,
            'age_to': age + up_age,
            'city': self.get_id_city(user_id),
            'status': '1' or '6',
            'has_photo': '1',
            'sort': '0',
            'fields': 'is_closed, id, first_name, last_name, city, bdate, sex',
            'count': count
        }
        response = requests.get(url, params={**self.params_User, **params}).json()
        return response

    def send_foto(self, user_id, user_id_foto, message=''):
        photos = ''
        for key, value in self.foto_dict(user_id_foto).items():
            photos += f'photo{value},'
        print(photos)
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'attachment': f'{photos}',
                                         'random_id': 0})
