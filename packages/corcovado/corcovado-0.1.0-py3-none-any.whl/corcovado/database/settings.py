from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import *

engine = create_engine("sqlite:///corcovado.sqlite")

db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def make_session(engine):
    return scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


Base = declarative_base()
