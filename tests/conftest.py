import os
import pytest
import functools

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from models.base import Base
import models.users
import models.customer
import models.element_administratif

load_dotenv()

url_object = URL.create(
    os.getenv("DATABASE_TYPE"),
    username=os.getenv("USERNAME_DB"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE_NAME"),
)

engine = create_engine(url_object)


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base
