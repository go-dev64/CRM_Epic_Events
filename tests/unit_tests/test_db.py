import pytest
import app.query_db as query_db


class TestDatabase:
    def test_database_connection(self):
        # test try to connect to database
        try:
            engine = query_db.database_engine()
            connection = engine.connect()
            assert connection is not None
        except Exception as e:
            pytest.fail(f"Échec de la connexion à la base de données : {e}")
