import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from crm.models.base import Base
import crm.models.users
import crm.models.customer
import crm.models.element_administratif


import argon2

ph = argon2.PasswordHasher()

load_dotenv()

URL_OBJECT = URL.create(
    os.getenv("DATABASE_TYPE"),
    username=os.getenv("USERNAME_DB"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE_NAME"),
)


class Database:
    def database_engine(self):
        engine = create_engine(URL_OBJECT)
        return engine

    def create_session(self):
        engine = self.database_engine()
        Session = sessionmaker(bind=engine)
        return Session

    def create_tables(self):
        engine = self.database_engine()
        Base.metadata.create_all(engine)

    def create_popultaes(self, session):
        password_manager1 = ph.hash("Password@1", salt=None)
        manager1 = crm.models.users.Manager(
            name="manager 1", email_address="manager_1@gmail.com", phone_number="+0335651", password=password_manager1
        )
        password_manager2 = ph.hash("Password@1", salt=None)
        manager2 = crm.models.users.Manager(
            name="manager 2", email_address="manager_2@gmail.com", phone_number="+0335651", password=password_manager2
        )
        password_seller = ph.hash("Password@1")
        seller1 = crm.models.users.Seller(
            name="seller 1", email_address="seller_1@gmail.com", phone_number="+0335651", password=password_seller
        )
        password_seller = ph.hash("Password@1")
        seller2 = crm.models.users.Seller(
            name="seller 2", email_address="seller_2@gmail.com", phone_number="+0335651", password=password_seller
        )
        password_supporter = ph.hash("Password@1")
        supporter1 = crm.models.users.Supporter(
            name="supporter 1",
            email_address="supporter@gmail.com",
            phone_number="+0335651",
            password=password_supporter,
        )
        password_supporter = ph.hash("Password@1")
        supporter2 = crm.models.users.Supporter(
            name="supporter 2",
            email_address="supporter2@gmail.com",
            phone_number="+0335651",
            password=password_supporter,
        )
        session.add_all([manager1, manager2, seller1, seller2, supporter1, supporter2])
        session.commit()
