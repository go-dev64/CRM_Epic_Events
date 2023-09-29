from datetime import datetime
import os
import pytest
from argon2 import PasswordHasher

from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from crm.models.users import Contract, Customer, Event, Manager, Seller, Supporter, User
from crm.models.authentication import Authentication
from crm.models.element_administratif import Address
from crm.models.utils import Utils

load_dotenv()

ph = PasswordHasher()

url_object = URL.create(
    os.getenv("DATABASE_TYPE"),
    username=os.getenv("USERNAME_DB"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE_NAME"),
)

Session = sessionmaker()
engine = create_engine(url_object)


@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    trans = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="function")
def users(db_session):
    password_manager = ph.hash("password_manager")
    manager = Manager(
        name="manager", email_address="manager@gmail.com", phone_number="+0335651", password=password_manager
    )
    password_seller = ph.hash("password_seller")
    seller = Seller(name="seller", email_address="seller@gmail.com", phone_number="+0335651", password=password_seller)
    password_supporter = ph.hash("password_supporter")
    supporter = Supporter(
        name="supporter", email_address="supporter@gmail.com", phone_number="+0335651", password=password_supporter
    )
    db_session.add_all([manager, seller, supporter])
    db_session.commit()
    return manager, seller, supporter


@pytest.fixture(scope="function")
def clients(db_session, users):
    users = users
    db_session.commit()
    client_1 = Customer(
        name="client_1",
        email_address="clien_1@123.com",
        phone_number="123456",
        company="7eme_company",
        seller_contact=users[1],
    )
    client_2 = Customer(
        name="client_2",
        email_address="clien_2@123.com",
        phone_number="123456",
        company="7eme_company",
        seller_contact=users[1],
    )
    db_session.add_all([client_1, client_2])
    db_session.commit()
    return client_1, client_2


@pytest.fixture(scope="function")
def contracts(db_session, users, clients):
    users = users
    clients = clients
    contract_1 = Contract(total_amount=1000, remaining=0, signed_contract=True, customer=clients[0], seller=users[1])
    contract_2 = Contract(
        total_amount=1000, remaining=5000, signed_contract=False, customer=clients[0], seller=users[1]
    )
    db_session.add_all([contract_1, contract_2])
    db_session.commit()
    return contract_1, contract_2


@pytest.fixture(scope="function")
def address(db_session, contracts):
    contracts
    address = Address(number=1, street="street", city="city", postal_code=1234, country="wftrt")
    db_session.add_all([address])
    db_session.commit()
    return address


@pytest.fixture(scope="function")
def events(db_session, contracts, users, clients, address):
    users = users
    clients = clients
    contracts = contracts
    address = address
    event_1 = Event(
        name="Event_1",
        date_start=datetime(2023, 9, 8, 15, 30),
        date_end=datetime(2023, 9, 9, 15, 30),
        attendees=10,
        note="nn",
        customer=clients[0],
        contract=contracts[0],
        address=address,
        supporter=None,
    )

    event_2 = Event(
        name="Event_2",
        date_start=datetime(2023, 9, 8, 15, 30),
        date_end=datetime(2023, 9, 9, 15, 30),
        attendees=10,
        note="nn",
        customer=clients[0],
        contract=contracts[0],
        address=address,
        supporter=users[2],
    )
    db_session.add_all([event_1, event_2])
    db_session.commit()
    return event_1, event_2


@pytest.fixture(scope="function")
def current_user_is_user(db_session):
    users
    user = db_session.scalars(select(User)).first()
    user = Authentication.get_token(user)
    db_session.current_user = user
    db_session.current_user_department = Utils().get_type_of_user(user)
    return db_session.current_user


@pytest.fixture(scope="function")
def current_user_is_manager(db_session):
    users
    user = db_session.scalars(select(Manager)).first()
    user = Authentication.get_token(user)
    db_session.current_user = user
    db_session.current_user_department = Utils().get_type_of_user(user)
    return db_session.current_user


@pytest.fixture(scope="function")
def current_user_is_seller(db_session):
    users
    user = db_session.scalars(select(Seller)).first()
    user = Authentication.get_token(user)
    db_session.current_user = user
    db_session.current_user_department = Utils().get_type_of_user(user)
    return db_session.current_user


@pytest.fixture(scope="function")
def current_user_is_supporter(db_session):
    users
    user = db_session.scalars(select(Supporter)).first()
    user = Authentication.get_token(user)
    db_session.current_user = user
    db_session.current_user_department = Utils().get_type_of_user(user)
    return db_session.current_user
