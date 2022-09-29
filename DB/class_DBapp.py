from sqlalchemy import func
import json


class DBapp:
    def __init__(self, User, Match, Favoritelist, Unfavoritelist, SearchingList, session, conn):
        self.user = User
        self.match = Match
        self.favoritelist = Favoritelist
        self.unfavoritelist = Unfavoritelist
        self.searchinglist = SearchingList
        self.session = session
        self.conn = conn
        self.offset = 0
        self.last = 0

    def __drop_create_searching_list(self):
        with self.conn.cursor() as cur:
            cur.execute('''
            DROP TABLE searching_list;
            ''')
            cur.execute('''CREATE TABLE IF NOT EXISTS searching_list(
            id SERIAL PRIMARY KEY,
            vk_id VARCHAR(20) UNIQUE,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            sex VARCHAR(10),
            age VARCHAR(10),
            city VARCHAR(50)
            );''')
            self.conn.commit()

    def __query_searching_list(self):
        query = self.session.query(self.searchinglist).filter(self.searchinglist.id == self.offset)
        for row in query:
            return [row.vk_id, row.first_name, row.last_name, row.age, row.sex, row.city]

    def add_to_searching_list(self, filepath):
        self.__drop_create_searching_list()
        with open(filepath, 'r') as f:
            data = json.loads(f.read())
            for vk_id, info in data.items():
                item = self.searchinglist(
                    vk_id=vk_id,
                    first_name=info['first_name'],
                    last_name=info['last_name'],
                    age=info['age'],
                    sex=info['sex'],
                    city=info['city']
                )
                self.session.add(item)
        self.session.commit()
        self.last = self.session.query(func.max(self.searchinglist.id)).all()[0][0]

    def get_next_search(self):  # Возвращает следующее значение бд списоком из 6и наименований
        if self.offset != self.last:
            self.offset += 1
            return self.__query_searching_list()
        return 'no more'

    def get_previous_search(self):  # Возвращает предыдущее значение бд списоком из 6и наименований
        if self.offset != 1 and self.offset != 0:
            self.offset -= 1
            return self.__query_searching_list()
        return 'no previous'

    def add_user(self, user_id):
        new_user = self.user(user_vk_id=user_id)
        self.session.add(new_user)
        self.session.commit()

    def add_match(self, match_id):
        pass

    def get_user_pk(self, vk_id):
        pass

    def get_match_pk(self, vk_id):
        pass

    def add_match_to_favorite(self, match_pk, user_pk):
        pass

    def add_match_to_unfavorite(self, match_pk, user_pk):
        pass

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
