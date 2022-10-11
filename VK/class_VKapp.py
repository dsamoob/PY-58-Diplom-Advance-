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

    def get_all(self, match_id: int, offset=0) -> (int, dict):
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'owner_id': match_id, 'extended': '1', 'photo_sizes': '1', 'offset': offset}
        response = requests.get(url, params={**self.params_User, **params}).json()
        result = response['response']['count']
        print(f'ВК get_all: получен json всех фотографий')
        return (result, response)

    def get_first(self, match_id: int, offset=0) -> (int, dict):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': match_id, 'album_id': "profile", 'extended': '1', 'photo_sizes': '1', 'offset': offset}
        response = requests.get(url, params={**self.params_User, **params}).json()
        result = response['response']['count']
        print(f'ВК get_first: получен json фотографий по альбому profile')
        return (result, response)

    def send_photo(self, user_id: int, match_id: int, message=''):
        photos = ''
        result = self.photo_dic(match_id).items()
        if result == 0:
            return 0
        for key, value in self.photo_dic(match_id).items():
            photos += f'{value},'
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'attachment': f'{photos}',
                                         'random_id': 0})
        print(f'ВК фотографии отправлены')
    def photo_dic(self, match_id:int ) -> dict:
        result = self.user_photo(match_id)
        dic = {}
        if result != 0:
            for i in result['response']['items']:
                dic[i["likes"]["count"]] = f'photo{i["owner_id"]}_{i["id"]}'
            if len(dic) >= 3:
                print(f'ВК возвращены 3 фотографии с наибольшим количеством лайков')
                return {x: dic[x] for x in sorted(dic)[::-1][0:3]}
        return 0

    def user_photo(self, match_id: int) -> dict:
        result_pro = self.get_first(match_id)
        result_all = self.get_all(match_id)
        if result_pro[0] in [0, 1]:
            if result_all[0] < 500:
                print(f'ВК user_photo: фотографий у пользователя менее 500 из photos.getAll')
                return result_all[1]
            else:
                print(f'ВК user_photo фотографий слишком много ')
                return 0
        elif result_pro[0] < 500:
            print(f'ВК user_photo: фотографий у пользователя менее 500 из photos.get(Profile)')
            return result_pro[1]
        print(f'ВК user_photo фотографий слишком много ')
        return 0

    def total_dict(self, user_id: int) -> dict:
        tot_dict = {}
        response = self.search_user(user_id)
        if response.get('response') is not None:
            print(f'ВК total_dict: входящий массив совпадений {len(response["response"]["items"])}')
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
            print(f'ВК total_dict: обработанный масив для загрузки {len(tot_dict)}')
            return tot_dict

    def search_user(self, user_id: int, down_age=1, up_age=1, count=1000) -> dict:  # Вывод найденных пользователе
        """ПОИСК ПОЛЬЗОВАТЕЛЯ ПО ДАННЫМ"""
        age = self.get_age(user_id)
        city = self.get_id_city(user_id)
        url = f'https://api.vk.com/method/users.search'
        params = {
            'sex': self.get_reverse_sex(user_id),
            'age_from': age - down_age,
            'age_to': age + up_age,
            'city': city,
            'status': '1' or '6',
            'has_photo': '1',
            'sort': '0',
            'fields': 'is_closed, id, first_name, last_name, city, bdate, sex',
            'count': count
        }
        response = requests.get(url, params={**self.params_User, **params}).json()
        return response


