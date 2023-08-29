import os
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from models.customer import Base


load_dotenv()


def database_engine():
    url_object = URL.create(
        os.getenv("DATABASE_TYPE"),
        username=os.getenv("USERNAME_DB"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE_NAME"),
    )
    engine = create_engine(url_object, echo=True)
    return engine


def create_session():
    engine = database_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_tables():
    engine = database_engine()
    metadata = Base.metadata

    # Utilisez sorted_tables pour obtenir la liste des tables dans l'objet MetaData
    tables = sorted(metadata.tables.values(), key=lambda table: table.name)

    # Affichez les noms des tables
    for table in tables:
        print("Table Name:", table.name)
    Base.metadata.create_all(engine)


# create_tables()
