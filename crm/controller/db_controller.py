import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, select
from sqlalchemy.orm import sessionmaker

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

    def create_default_manager(self, db_session):
        with db_session.begin() as session:
            number_of_user = len(session.scalars(select(crm.models.users.User)).all())
            if number_of_user == 0:
                password_manager1 = ph.hash(os.getenv("PASSWORD_MANAGER"))
                manager1 = crm.models.users.Manager(
                    name="manager 1",
                    email_address=os.getenv("EMAIL"),
                    phone_number="+0335651",
                    password=password_manager1,
                )
                session.add_all([manager1])
                session.commit()
