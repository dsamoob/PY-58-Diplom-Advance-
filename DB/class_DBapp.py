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

    def __query_searching_list(self, index):
        query = self.session.query(self.searchinglist).filter(self.searchinglist.id == index)
        for row in query:
            return [row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city]

    """Удаляет из поискового списка в бд все соответствия по пользователю"""

    def __del_from_sl_user(self, vk_id):
        self.session.query(self.searchinglist).where(self.searchinglist.user_id == str(vk_id)).delete()
        self.session.commit()

    """Формирает список вк ид из черного списка и списка избранных"""

    def __ids_from_lists(self, user_id):
        check_list = []  #
        for item in self.get_favorite_list(user_id):
            check_list.append(item[0])
        for item in self.get_unfavorite_list(user_id):
            check_list.append(item[0])
        return check_list

    """Добавление в бд списка соответствий"""

    def add_to_searching_list(self, match_dic, user_id):
        self.__del_from_sl_user(user_id)  # удаляет из бд список соответствий используемый данным пользователем ранее
        check_list = self.__ids_from_lists(
            user_id)  # создакт список вк ид по пользователю из его черного и белого списков
        for match_id, info in match_dic.items():
            if str(match_id) not in check_list:
                item = self.searchinglist(
                    user_id=str(user_id),
                    match_id=match_id,
                    first_name=info['first_name'],
                    last_name=info['last_name'],
                    age=info['age'],
                    sex=info['sex'],
                    city=info['city']
                )
                self.session.add(item)
        self.session.commit()


    def set_user_log(self, user_id):
        first = self.session.query(func.min(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                                str(user_id)).all()[0][0]
        last = self.last = self.session.query(func.max(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                               str(user_id)).all()[0][0]
        self.session.query(self.user).filter(self.user.vk_id == str(user_id)).update({'first': first,
                                                                                 'actual': first,
                                                                                 'last': last})
        self.session.commit()


    """Устанавливает и возвращает первое соответствие для пользователя и выдает его"""
    def get_match(self, index):
        query = self.session.query(self.searchinglist).filter(self.searchinglist.id == str(index))
        for row in query:
            return [row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city]

    def get_first_search(self, user_id):
        index = self.session.query(self.user.first).filter(self.user.vk_id == str(user_id)).all()
        return self.__query_searching_list(index[0][0])


    """Выдает следующее соответствие"""

    def get_next_search(self, user_id):
        self.session.query(self.user).filter(self.user.vk_id == str(user_id)).update({'actual': self.user.actual + 1})
        self.session.commit()
        index = self.session.query(self.user.actual).filter(self.user.vk_id == str(user_id)).all()
        return self.__query_searching_list(index[0][0])


    """Выдает предыдущее соответствие"""

    def get_previous_search(self, user_id):
        first = self.session.query(self.user.first).filter(self.user.vk_id == str(user_id)).all()
        actual = self.session.query(self.user.actual).filter(self.user.vk_id == str(user_id)).all()
        print(first[0][0])
        print(actual[0][0])
        if first[0][0] >= actual[0][0]:
            return 0
        self.session.query(self.user).filter(self.user.vk_id == str(user_id)).update({'actual': self.user.actual - 1})
        self.session.commit()
        index = self.session.query(self.user.actual).filter(self.user.vk_id == str(user_id)).all()
        return self.__query_searching_list(index[0][0])

    """Добавляет пользователя в БД"""

    def get_actual_index(self, user_id):
        actual = self.session.query(self.user.actual).filter(self.user.vk_id == str(user_id)).one()
        return actual[0]

    def get_user_id_by_id(self, id):
        result = self.session.query(self.searchinglist.match_id).filter(self.searchinglist.id == id).one()
        return result[0]

    def add_user(self, user_id):
        user_id = str(user_id)
        try:
            self.session.query(self.user).filter(self.user.vk_id == user_id).one()
        except:
            new_user = self.user(vk_id=user_id)
            self.session.add(new_user)
            self.session.commit()

    """Добавляет соответствие в БД"""

    def add_match(self, match_id):
        match_id = str(match_id)
        try:
            self.session.query(self.match).filter(self.match.vk_id == match_id).one()
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

    """Получает ПК пользователя"""

    def __get_user_pk(self, vk_id):
        user = self.session.query(self.user).filter(self.user.vk_id == str(vk_id))
        for item in user:
            return item.id

    """Получает ПК соответствия"""

    def __get_match_pk(self, vk_id):
        match = self.session.query(self.match).filter(self.match.vk_id == str(vk_id))
        for i in match:
            return i.id

    """Добавляет в список избранных ПК пользователя и ПК соотвествия"""

    def add_match_to_favorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        add = self.favoritelist(id_user=upk,
                                id_match=mpk)
        self.session.add(add)
        self.session.commit()

    """Добавляет в черный список ПК пользовтеля и ПК соотвествия"""

    def add_match_to_unfavorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        add = self.unfavoritelist(id_user=upk,
                                  id_match=mpk)
        self.session.add(add)
        self.session.commit()

    """Выдает список избранных по пользовтелю"""

    def get_favorite_list(self, user_id):
        favorite_list = []
        pk = self.__get_user_pk(user_id)
        favorites = [i.id_match for i in self.session.query(self.favoritelist).filter(self.favoritelist.id_user == pk)]
        for item in favorites:
            for row in self.session.query(self.match).filter(self.match.id == item).all():
                favorite_list.append([row.vk_id, row.first_name, row.last_name, row.sex, row.age, row.city])
        return favorite_list

    """Выдает черный список по пользовтелю"""

    def get_unfavorite_list(self, user_id):
        unfavorite_list = []
        upk = self.__get_user_pk(user_id)
        favorites = [i.id_match for i in
                     self.session.query(self.unfavoritelist).filter(self.unfavoritelist.id_user == upk)]
        for item in favorites:
            for row in self.session.query(self.match).filter(self.match.id == item).all():
                unfavorite_list.append([row.vk_id, row.first_name, row.last_name, row.sex, row.age, row.city])
        return unfavorite_list

    """Удаляет из списка избранных"""

    def del_from_favorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        self.session.query(self.favoritelist).filter(
            self.favoritelist.id_user == upk).filter(self.favoritelist.id_match == mpk).delete()
        self.session.commit()

    """Удаляет из черного списка"""

    def del_from_unfavorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        self.session.query(self.unfavoritelist).filter(
            self.unfavoritelist.id_user == upk).filter(self.unfavoritelist.id_match == mpk).delete()
        self.session.commit()
