import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def database_engine():
    database_url = os.environ.get("DATABASE_URL")
    engine = create_engine(database_url)
    return engine
