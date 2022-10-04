from sqlalchemy import func
import json


class DBapp:
    def __init__(self, User, Match, Favoritelist, Unfavoritelist, SearchingList, session):
        self.user = User
        self.match = Match
        self.favoritelist = Favoritelist
        self.unfavoritelist = Unfavoritelist
        self.session = session
        self.searchinglist = SearchingList
        self.offset = 0
        self.last = 0

    def __query_searching_list(self):
        query = self.session.query(self.searchinglist).filter(self.searchinglist.id == self.offset)
        for row in query:
            return [row.match_id, row.first_name, row.last_name, row.age, row.sex, row.city]

    def __del_from_sl_user(self, vk_id):
        for_delete = self.session.query(self.searchinglist).where(self.searchinglist.user_id == str(vk_id)).delete()
        self.session.commit()

    def add_to_searching_list(self, match_dic, user_id):
        self.__del_from_sl_user(user_id)
        check_list = []
        for item in self.get_favorite_list(user_id):
            check_list.append(item[0])
        for item in self.get_unfavorite_list(user_id):
            check_list.append(item[0])
        print(check_list)
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


        self.last = self.session.query(func.max(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                               str(user_id)).all()[0][0]


    def get_first_search(self, user_id):
        self.offset = self.session.query(func.min(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                                 str(user_id)).all()[0][0]
        result = result = self.__query_searching_list()
        return result

    def get_next_search(self):  # Возвращает следующее значение бд списоком из 6и наименований
        if self.offset != self.last:
            self.offset += 1
            result = self.__query_searching_list()
            return result
        return 'no more'

    def get_previous_search(self):  # Возвращает предыдущее значение бд списоком из 6и наименований
        if self.offset != 1 and self.offset != 0:
            self.offset -= 1
            result = self.__query_searching_list()
            return result
        return 'no more'

    def add_user(self, user_id):
        user_id = str(user_id)
        try:
            new_user = self.session.query(self.user).filter(self.user.vk_id == user_id).one()
        except:
            new_user = self.user(vk_id=user_id)
            self.session.add(new_user)
            self.session.commit()

    def add_match(self, match_id):
        match_id = str(match_id)
        try:
            new_match = self.session.query(self.match).filter(self.match.vk_id == match_id).one()
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

    def __get_user_pk(self, vk_id):
        user = self.session.query(self.user).filter(self.user.vk_id == str(vk_id))
        for item in user:
            return item.id

    def __get_match_pk(self, vk_id):
        match = self.session.query(self.match).filter(self.match.vk_id == str(vk_id))
        for i in match:
            return i.id

    def add_match_to_favorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        add = self.favoritelist(id_user=upk,
                                id_match=mpk)
        self.session.add(add)
        self.session.commit()

    def add_match_to_unfavorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        add = self.unfavoritelist(id_user=upk,
                                  id_match=mpk)
        self.session.add(add)
        self.session.commit()

    def get_favorite_list(self, user_id):
        favorite_list = []
        pk = self.__get_user_pk(user_id)
        favorites = [i.id_match for i in self.session.query(self.favoritelist).filter(self.favoritelist.id_user == pk)]
        for item in favorites:
            for row in self.session.query(self.match).filter(self.match.id == item).all():
                favorite_list.append([row.vk_id, row.first_name, row.last_name, row.sex, row.age, row.city])
        return favorite_list

    def get_unfavorite_list(self, user_id):
        unfavorite_list = []
        upk = self.__get_user_pk(user_id)
        favorites = [i.id_match for i in self.session.query(self.unfavoritelist).filter(self.unfavoritelist.id_user == upk)]
        for item in favorites:
            for row in self.session.query(self.match).filter(self.match.id == item).all():
                unfavorite_list.append([row.vk_id, row.first_name, row.last_name, row.sex, row.age, row.city])
        return unfavorite_list

    def del_favorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        for_delete = self.session.query(self.favoritelist).filter(
            self.favoritelist.id_user == upk).filter(self.favoritelist.id_match == mpk).delete()
        self.session.commit()

    def del_unfavorite(self, user_id, match_id):
        upk = self.__get_user_pk(user_id)
        mpk = self.__get_match_pk(match_id)
        for_delete = self.session.query(self.unfavoritelist).filter(
            self.unfavoritelist.id_user == upk).filter(self.unfavoritelist.id_match == mpk).delete()
        self.session.commit()



    def __check_dupl_fav_unfav(self, upk, mpk, table):
        pass
