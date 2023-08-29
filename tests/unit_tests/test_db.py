import pytest
import controllers.db_controller as db_controller
from sqlalchemy import inspect


class TestDatabase:
    def test_database_connection(self):
        # test try to connect to database
        try:
            engine = db_controller.database_engine()
            connection = engine.connect()
            assert connection is not None
        except Exception as e:
            pytest.fail(f"Échec de la connexion à la base de données : {e}")

    def test_create_table(self):
        tables_models = [
            "supporter_table",
            "manager_table",
            "seller_table",
            "event_table",
            "contract_table",
            "address_table",
            "company_table",
            "customer_table",
        ]
        db_controller.create_tables()
        engine = db_controller.database_engine()
        inspector = inspect(engine)
        tables_db = inspector.get_table_names()
        assert len(tables_models) == len(tables_db)
        for t in tables_db:
            assert t in tables_models

    def test_create_manager(self):
        pass

    def test_create_seller(self):
        pass

    def test_create_supporter(self):
        pass
