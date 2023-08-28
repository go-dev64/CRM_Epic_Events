import pytest
import controllers.db_controller as db_controller


class TestDatabase:
    def test_database_connection(self):
        # test try to connect to database
        try:
            engine = db_controller.database_engine()
            connection = engine.connect()
            assert connection is not None
        except Exception as e:
            pytest.fail(f"Échec de la connexion à la base de données : {e}")
