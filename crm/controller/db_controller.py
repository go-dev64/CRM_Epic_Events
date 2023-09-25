import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

from crm.models.base import Base
import crm.models.users
import crm.models.customer
import crm.models.element_administratif


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
        session = Session()
        return session

    def create_tables(self):
        engine = self.database_engine()
        Base.metadata.create_all(engine)
