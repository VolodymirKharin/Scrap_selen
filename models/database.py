from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models.config import *

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST_DB}:{PORT_DB}/{DB_NAME}"
)

Base = declarative_base()


def create_db():
    Base.metadata.create_all(engine)


def del_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    create_db()


