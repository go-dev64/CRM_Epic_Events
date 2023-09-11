from datetime import datetime
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
def users(db_session):
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
    db_session.add_all([manager, seller, supporter])
    db_session.commit()
    yield


@pytest.fixture(scope="function")
def clients(db_session, users):
    users
    client_1 = crm_app.user.models.users.Customer(
        name="client_1",
        email_address="clien_1@123.com",
        phone_number="123456",
        company="7eme_company",
        seller_contact_id=2,
    )
    client_2 = crm_app.user.models.users.Customer(
        name="client_2", email_address="clien_2@123.com", phone_number="123456", company="7eme_company"
    )
    db_session.add_all([client_1, client_2])
    db_session.commit()
    yield


@pytest.fixture(scope="function")
def contracts(db_session, users):
    users
    contract_1 = crm_app.user.models.users.Contract(
        total_amount=1000, remaining=5000, signed_contract=True, customer_id=5, seller_id=2
    )
    contract_2 = crm_app.user.models.users.Contract(
        total_amount=1000, remaining=5000, signed_contract=False, customer_id=1, seller_id=1
    )
    db_session.add_all([contract_1, contract_2])
    db_session.commit()
    yield


@pytest.fixture(scope="function")
def events(db_session, users):
    users
    event_1 = crm_app.user.models.users.Event(
        name="Event_1",
        date_start=datetime(2023, 9, 8, 15, 30),
        date_end=datetime(2023, 9, 9, 15, 30),
        attendees=10,
        note="nn",
        customer_id=1,
        contract_id=1,
        address_id=1,
    )

    event_2 = crm_app.user.models.users.Event(
        name="Event_2",
        date_start=datetime(2023, 9, 8, 15, 30),
        date_end=datetime(2023, 9, 9, 15, 30),
        attendees=10,
        note="nn",
        customer_id=1,
        contract_id=1,
        address_id=1,
    )
    db_session.add_all([event_1, event_2])
    db_session.commit()
    yield
