from datetime import datetime
import requests
import vk_api
from vk_api.longpoll import VkLongPoll
import json

class VKapp:
    def __init__(self, token_user, tokenVK_Group, version='5.131'):
        self.token_user = token_user
        self.tokenVK_Group = tokenVK_Group
        self.version = version
        self.paramsVK_Group = {'access_token': self.tokenVK_Group, 'v': self.version}
        self.params_User = {'access_token': self.token_user, 'v': self.version}
        self.vk = vk_api.VkApi(token=tokenVK_Group)  # АВТОРИЗАЦИЯ СООБЩЕСТВА
        self.vk_session = vk_api.VkApi(token=tokenVK_Group)
        self.session_api = self.vk_session.get_api()
        self.longpoll = VkLongPoll(self.vk)  # РАБОТА С СООБЩЕНИЯМИ
        self.dict_cash = {}

    def send_msg(self, user_id, some_text):
        self.vk_session.method("messages.send", {"user_id": user_id, "message": some_text, "random_id": 0})

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
        try:
            date = response['response'][0]['bdate']
            year = datetime.now().year
            return year - datetime.strptime(date, '%d.%m.%Y').year
        except KeyError:
            self.send_msg(user_id, 'Ошибка токена')

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
        # time.sleep(0.3)
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
            # pprint(response)
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

    def search_user(self, user_id, down_adge=1, up_adge=1, count=1000):  # Вывод найденных пользователе
        """ПОИСК ПОЛЬЗОВАТЕЛЯ ПО ДАННЫМ"""
        url = f'https://api.vk.com/method/users.search'
        params = {
            'sex': self.get_reverse_sex(user_id),
            'age_from': self.get_age(user_id) - down_adge,
            'age_to': self.get_age(user_id) + up_adge,
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
        for key, value in self.foto_dict(user_id_foto).items():
            self.vk.method('messages.send', {'user_id': user_id,
                                                 'message': message,
                                                 'attachment': f'photo{value}',
                                                 'random_id': 0})

