import os
import sqlmodel
from sqlmodel import SQLModel, Session


DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL == "":
    raise NotImplementedError("DATABASE_URL needs to be set")


engine = sqlmodel.create_engine(DATABASE_URL)


def init_db():
    # create database times
    # print("creating db")
    SQLModel.metadata.create_all(engine)



def get_session():
    # use within routes or api endpoints
    with Session(engine) as session:
        yield session