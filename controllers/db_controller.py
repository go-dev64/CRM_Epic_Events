import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.customer import Base


load_dotenv()


def database_engine():
    database_url = os.environ.get("DATABASE_URL")
    engine = create_engine(database_url, echo=True)
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


create_tables()
