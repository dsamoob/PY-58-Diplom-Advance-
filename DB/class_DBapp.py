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

    def __delete_from_searching_list(self, vk_id):
        for_delete = self.session.query(self.searchinglist).where(self.searchinglist.user_id == str(vk_id)).delete()
        self.session.commit()


    def add_to_searching_list(self, match_dic, user_id):
        self.__delete_from_searching_list(user_id)
        for match_id, info in match_dic.items():
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
        self.offset = self.session.query(func.min(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                                 str(user_id)).all()[0][0]
        self.last = self.session.query(func.max(self.searchinglist.id)).filter(self.searchinglist.user_id ==
                                                                               str(user_id)).all()[0][0]

    def get_next_search(self):  # Возвращает следующее значение бд списоком из 6и наименований
        if self.offset != self.last:
            result = self.__query_searching_list()
            self.offset += 1
            return result
        return 'no more'

    def get_previous_search(self):  # Возвращает предыдущее значение бд списоком из 6и наименований
        if self.offset != 1 and self.offset != 0:
            self.offset -= 1
            return self.__query_searching_list()
        return 'no previous'

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
        user = self.session.query(self.user).filter(self.user.vk_id == vk_id)
        for i in user:
            return i.id

    def __get_match_pk(self, vk_id):
        match = self.session.query(self.match).filter(self.match.vk_id == vk_id)
        for i in match:
            return i.id

    def add_match_to_favorite(self, user_id, match_id):
        user_pk = self.__get_user_pk(str(user_id))
        match_pk = self.__get_match_pk(str(match_id))
        add = self.favoritelist(id_user=user_pk,
                                id_match=match_pk)
        self.session.add(add)
        self.session.commit()


    def add_match_to_unfavorite(self, user_id, match_id):
        user_pk = self.__get_user_pk(str(user_id))
        match_pk = self.__get_match_pk(str(match_id))
        add = self.unfavoritelist(id_user=user_pk,
                                  id_match=match_pk)
        self.session.add(add)
        self.session.commit()

    def del_unfavorite(self, vk_user_id, vk_match_id):
        pass

    def del_favorite(self, vk_user_id, vk_match_id):
        pass

    def get_favorite_list(self, user_pk):
        pass

    def get_unfavorite_list(self, user_pk):
        pass

    def check_duplicates(self, vk_match_id, table):
        pass
