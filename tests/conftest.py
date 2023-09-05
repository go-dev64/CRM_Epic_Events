import os
import pytest
import functools
from argon2 import PasswordHasher

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv
from crm_app.user.models.base import Base
import crm_app.user.models.users
import crm_app.crm.models.customer
import crm_app.crm.models.element_administratif

load_dotenv()

ph = PasswordHasher()

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


@pytest.fixture(scope="function")
def db_session(mocked_session):
    session = mocked_session
    yield session
    session.rollback()
    session.close()


@pytest.fixture(scope="function")
def users():
    password_manager = ph.hash("password_manager")
    manager = crm_app.user.models.users.Manager(
        name="manager", email_address="manager@gmail.com", phone_number="+0335651", password=password_manager
    )
    password_seller = ph.hash("password_seller")
    seller = crm_app.user.models.users.Seller(
        name="seller", email_address="seller@gmail.com", phone_number="+0335651", password=password_seller
    )
    password_supporter = ph.hash("password_supporter")
    supporter = crm_app.user.models.users.Supporter(
        name="supporter", email_address="supporter@gmail.com", phone_number="+0335651", password=password_supporter
    )
    return [manager, seller, supporter]
