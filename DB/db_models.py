import sqlalchemy as sq
from sqlalchemy.orm import declarative_base

Base = declarative_base()

""" отдельная таблица для прохода по найденым результатам"""
class SearchingList(Base):
    __tablename__ = "searching_list"
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer)
    match_id = sq.Column(sq.Integer)
    first_name = sq.Column(sq.String(length=50))
    last_name = sq.Column(sq.String(length=50))
    sex = sq.Column(sq.String(length=10))
    age = sq.Column(sq.String(length=10))
    city = sq.Column(sq.String(length=50))


"""таблица пользователей"""
class User(Base):
    __tablename__ = "user"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first = sq.Column(sq.Integer)
    actual = sq.Column(sq.Integer)
    last = sq.Column(sq.Integer)


"""таблица соотвествий, которые добавлялись в черный и/или белый списки"""
class Match(Base):
    __tablename__ = "match"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.Integer, unique=True)
    first_name = sq.Column(sq.String(length=50))
    last_name = sq.Column(sq.String(length=50))
    sex = sq.Column(sq.String(length=20))
    age = sq.Column(sq.String(length=10))
    city = sq.Column(sq.String(length=50))


"""Список избранных по пользователям"""
class FavoriteList(Base):
    __tablename__ = "favorite_list"

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=False)
    id_match = sq.Column(sq.Integer, sq.ForeignKey("match.id"), nullable=False)


"""черный список по пользователям"""
class UnFavoriteList(Base):
    __tablename__ = "unfavorite_list"

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=False)
    id_match = sq.Column(sq.Integer, sq.ForeignKey("match.id"), nullable=False)


def create_tables(engine):
    Base.metadata.drop_all(engine)
    print(f'БД: таблицы сброшены')
    Base.metadata.create_all(engine)
    print(f'БД: таблицы созданы')

