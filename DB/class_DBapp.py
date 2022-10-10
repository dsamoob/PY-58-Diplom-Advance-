from sqlalchemy import func
from DB.db_models import Match, User, FavoriteList, UnFavoriteList, SearchingList


class DBapp:
    def __init__(self, session):
        self.session = session
        self.user = User
        self.match = Match
        self.favoritelist = FavoriteList
        self.unfavoritelist = UnFavoriteList
        self.searchinglist = SearchingList
        self.offset = 0
        self.last = 0

    """Получает из списка ряд согласно ид в классе"""

    def __query_searching_list(self, index: int) -> list:
        query = self.session.query(self.searchinglist).filter(self.searchinglist.id == index)
        for row in query:
            print(f'БД __query_searching_list: найдено соотвествие поиску по {index}'
                  f' {row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city}')
            return [row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city]

    """Удаляет из поискового списка в бд все соответствия по пользователю"""

    def __del_from_sl_user(self, user_id: int):
        self.session.query(self.searchinglist).where(self.searchinglist.user_id == user_id).delete()
        self.session.commit()
        print(f'БД __del_from_sl_user: поисковая таблица для {user_id} очищена')


    """Формирает список вк ид из черного списка и списка избранных"""

    def __ids_from_lists(self, user_id: int) -> list:
        check_list = []  #
        for item in self.get_favorite_list(user_id):
            check_list.append(item[0])
        for item in self.get_unfavorite_list(user_id):
            check_list.append(item[0])
        print(
            f'БД __ids_from_lists: сформирован список длинной {len(check_list)} ид из черного и белого списков для пользователя {user_id}')
        return check_list

    """Добавление в бд списка соответствий"""

    def add_to_searching_list(self, match_dic: dict, user_id: int):
        self.__del_from_sl_user(user_id)  # удаляет из бд список соответствий используемый данным пользователем ранее
        check_list = self.__ids_from_lists(
            user_id)  # создакт список вк ид по пользователю из его черного и белого списков
        for match_id, info in match_dic.items():
            if match_id not in check_list:
                item = self.searchinglist(
                    user_id=user_id,
                    match_id=match_id,
                    first_name=info['first_name'],
                    last_name=info['last_name'],
                    age=info['age'],
                    sex=info['sex'],
                    city=info['city']
                )
                self.session.add(item)
        self.session.commit()
        print(f'БД add_to_searching_list: для пользователя {user_id} '
              f'обновлен список соотвествий на {len(match_dic) - len(check_list)} позиций')

    def set_user_log(self, user_id: int):
        first = self.session.query(func.min(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                           user_id).one()[0]
        last = self.last = self.session.query(func.max(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                                      user_id).one()[0]
        self.session.query(self.user).filter(self.user.vk_id == user_id).update({'first': first,
                                                                                 'actual': first,
                                                                                 'last': last})
        self.session.commit()
        print(f'БД set_user_log: для пользователя {user_id} установлены индексы {first, first, last}')

    """Устанавливает и возвращает первое соответствие для пользователя и выдает его"""


    def get_match(self, index: int) -> list:
        query = self.session.query(self.searchinglist).filter(self.searchinglist.id == index)
        for row in query:
            print(
                f'БД get_match: найдено соотвествие {row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city}')
            return [row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city]

    def get_first_search(self, user_id: int) -> list:
        index = self.get_first_index(user_id)
        return self.__query_searching_list(index)

    def get_first_index(self, user_id: int) -> int:
        index = self.session.query(self.user.first).filter(self.user.vk_id == user_id).one()[0]
        print(f'БД get_first_index: выявлен индекс первого {user_id}:{index}')
        return index

    def get_actual_index(self, user_id: int) -> int:
        index = self.session.query(self.user.actual).filter(self.user.vk_id == user_id).one()[0]
        print(f'БД get_actual_index: получен актуальный индекс для пользователя {user_id}:{index}')
        return index

    def get_last_index(self, user_id: int) -> int:
        index = self.last = self.session.query(func.max(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                                       user_id).one()[0]
        print(f'БД get_last_index: получен индекс последнего {user_id}:{index}')
        return index




    """Выдает следующее соответствие"""

    def get_next_search(self, user_id: int) -> list:
        first = self.get_first_index(user_id)
        actual = self.get_actual_index(user_id)
        last = self.get_last_index(user_id)
        if actual >= last:
            self.session.query(self.user).filter(self.user.vk_id == user_id).update({'actual': first})
            self.session.commit()
            index = self.get_actual_index(user_id)
            return self.__query_searching_list(index)
        self.session.query(self.user).filter(self.user.vk_id == user_id).update({'actual': self.user.actual + 1})
        self.session.commit()
        index = self.get_actual_index(user_id)
        print(f'БД get_next_search: обновлен текущий индекс для пользователя {user_id} {index}')
        return self.__query_searching_list(index)

    """Выдает предыдущее соответствие"""

    def get_previous_search(self, user_id: int) -> list:
        first = self.get_first_index(user_id)
        actual = self.get_actual_index(user_id)
        last = self.get_last_index(user_id)
        print(f'first: {first} actual: {actual}')
        if actual == 0 or actual == first:
            print(f' actual == 0 or == first {first, actual, last}')
            self.session.query(self.user).filter(self.user.vk_id == user_id).update({'actual': last})
            self.session.commit()
            index = self.get_actual_index(user_id)
            print(f'предоставление по индексу {index}')
            return self.__query_searching_list(index)
        self.session.query(self.user).filter(self.user.vk_id == user_id).update({'actual': self.user.actual - 1})
        self.session.commit()
        index = self.get_actual_index(user_id)
        print(f'БД get_previous_search: Обновлен текущий индекс для пользователя {user_id} {index}')
        print(f' предоставление по индексу {index}')
        return self.__query_searching_list(index)

    """Добавляет пользователя в БД"""

    def get_match_id_by_id(self, id: int) -> int:
        result = self.session.query(self.searchinglist.match_id).filter(self.searchinglist.id == id).one()[0]
        print(f'БД get_match_id_by_id: получен вк индекс по индексу {id} - {result}')
        return result

    def add_user(self, user_id: int) -> int:
        try:
            self.session.query(self.user).filter(self.user.vk_id == user_id).one()
            print(f'БД add_user: пользователь {user_id} уже есть в базе')
            return 0
        except:
            new_user = self.user(vk_id=user_id)
            self.session.add(new_user)
            self.session.commit()
            print(f'БД add_user: пользователь {user_id} добавлен в базу')
            return 1

    """Добавляет соответствие в БД"""

    def add_match(self, match_id: int) -> int:
        try:
            self.session.query(self.match).filter(self.match.vk_id == match_id).one()
            print(f'БД add_match: соотвествие {match_id} уже есть в базе')
        except:
            new_match = self.session.query(self.searchinglist).filter(self.searchinglist.match_id == match_id).all()
            for row in new_match:
                new_row = [row.first_name, row.last_name, row.sex, row.age, row.city]
                add = self.match(vk_id=match_id,
                                 first_name=new_row[0],
                                 last_name=new_row[1],
                                 sex=new_row[2],
                                 age=new_row[3],
                                 city=new_row[4]
                                 )
                self.session.add(add)
                self.session.commit()
                print(f'БД: соответствие {match_id} добавлено в базу')

    """Получает ПК пользователя"""

    def __get_user_pk(self, vk_id: int) -> int:
        user = self.session.query(self.user.id).filter(self.user.vk_id == vk_id).first()[0]
        print(f'БД __get_user_pk: получен ПК {user} для пользователя {vk_id}')
        return user

    """Получает ПК соответствия"""

    def __get_match_pk(self, vk_id: int) -> int:
        match = self.session.query(self.match.id).filter(self.match.vk_id == vk_id).first()[0]
        print(f'БД __get_match_pk: получен ПК {match} для соответствия {vk_id}')
        return match

    """Добавляет в список избранных ПК пользователя и ПК соотвествия"""

    def add_match_to_favorite(self, user_id: int, match_id: int):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        add = self.favoritelist(id_user=upk,
                                id_match=mpk)
        self.session.add(add)
        self.session.commit()
        print(f'БД add_match_to_favorite: в список избранных для пользователя {user_id} добавлен {match_id}')

    """Добавляет в черный список ПК пользовтеля и ПК соотвествия"""

    def add_match_to_unfavorite(self, user_id: int, match_id: int):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        add = self.unfavoritelist(id_user=upk,
                                  id_match=mpk)
        self.session.add(add)
        self.session.commit()
        print(f'БД add_match_to_unfavorite: в список черных для пользователя {user_id} добавлен {match_id}')

    """Выдает список избранных по пользовтелю"""

    def get_favorite_list(self, user_id: int) -> list:
        favorite_list = []
        pk = self.__get_user_pk(user_id)
        favorites = [i.id_match for i in self.session.query(self.favoritelist).filter(self.favoritelist.id_user == pk)]
        for item in favorites:
            for row in self.session.query(self.match).filter(self.match.id == item).all():
                favorite_list.append([row.vk_id, row.first_name, row.last_name, row.sex, row.age, row.city])
        print(f'БД get_favorite_list: получен список избранных для пользователя {user_id} длинной {len(favorites)}')
        return favorite_list

    """Выдает черный список по пользовтелю"""

    def get_unfavorite_list(self, user_id: int) -> list:
        unfavorite_list = []
        upk = self.__get_user_pk(user_id)
        favorites = [i.id_match for i in
                     self.session.query(self.unfavoritelist).filter(self.unfavoritelist.id_user == upk)]
        for item in favorites:
            for row in self.session.query(self.match).filter(self.match.id == item).all():
                unfavorite_list.append([row.vk_id, row.first_name, row.last_name, row.sex, row.age, row.city])
        print(f'БД get_unfavorite_list: получен черный список для пользователя {user_id} длинной {len(favorites)}')
        return unfavorite_list

    """Удаляет из списка избранных"""

    def del_from_favorite(self, user_id: int, match_id: int):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        self.session.query(self.favoritelist).filter(
            self.favoritelist.id_user == upk).where(self.favoritelist.id_match == mpk).delete()
        self.session.commit()
        print(f'БД del_from_favorite: {match_id} для пользователя {user_id} удален из списка избранных')

    """Удаляет из черного списка"""

    def del_from_unfavorite(self, user_id: int, match_id: int):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        self.session.query(self.unfavoritelist).filter(
            self.unfavoritelist.id_user == upk).where(self.unfavoritelist.id_match == mpk).delete()
        self.session.commit()

        print(f'БД del_from_unfavorite: {match_id} для пользователя {user_id} удален из черного списка')
