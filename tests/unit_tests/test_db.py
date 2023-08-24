import pytest
from sqlalchemy import create_engine


def test_database_connection():
    # test try to connect to database
    try:
        engine = database_engine()
        connection = engine.connect()
        assert connection is not None
    except Exception as e:
        pytest.fail(f"Échec de la connexion à la base de données : {e}")
