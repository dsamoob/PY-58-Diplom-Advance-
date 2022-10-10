import sqlalchemy
from sqlalchemy.orm import sessionmaker
import config as config
from DB.db_models import create_tables


DSN = f'postgresql://{config.db_login}:{config.db_password}@localhost:5432/{config.db_name}'
engine = sqlalchemy.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

"""Для теста"""
if __name__ == '__main__':
    create_tables(engine)

