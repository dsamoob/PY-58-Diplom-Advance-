import sqlalchemy as sq
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class SearchingList(Base):
    __tablename__ = "searching_list"
    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.String(length=20))
    match_id = sq.Column(sq.String(length=20), unique=True)
    first_name = sq.Column(sq.String(length=50))
    last_name = sq.Column(sq.String(length=50))
    sex = sq.Column(sq.String(length=10))
    age = sq.Column(sq.String(length=10))
    city = sq.Column(sq.String(length=50))


class User(Base):
    __tablename__ = "user"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String(length=80), unique=True)

    def __str__(self):
        return f'{self.id}: {self.user_vk_id}'


class Match(Base):
    __tablename__ = "match"

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.String(length=20), unique=True)
    first_name = sq.Column(sq.String(length=50))
    last_name = sq.Column(sq.String(length=50))
    sex = sq.Column(sq.String(length=20))
    edge = sq.Column(sq.String(length=10))
    city = sq.Column(sq.String(length=50))

    def __str__(self):
        return f'{self.id}: {self.vk_id}'




class FavoriteList(Base):
    __tablename__ = "favorite_list"

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=False)
    id_match = sq.Column(sq.Integer, sq.ForeignKey("match.id"), nullable=False)


class UnFavoriteList(Base):
    __tablename__ = "unfavorite_list"

    id = sq.Column(sq.Integer, primary_key=True)
    id_user = sq.Column(sq.Integer, sq.ForeignKey("user.id"), nullable=False)
    id_match = sq.Column(sq.Integer, sq.ForeignKey("match.id"), nullable=False)


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

