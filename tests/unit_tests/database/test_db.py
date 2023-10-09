import pytest
from sqlalchemy import select, text
from crm.controller.db_controller import Database
from crm.models.base import Base
import crm.models.users
import crm.models.customer
import crm.models.element_administratif
from tests.factory.user_factory import Manager

db = Database()


class TestDatabase:
    def test_database_connection_for_test(self, db_session):
        # test try to connect to database
        try:
            assert db_session is not None
        except Exception as e:
            pytest.fail(f"Échec de la connexion à la base de données : {e}")

    def test_metadata(self):
        tables_models = [
            "supporter_table",
            "manager_table",
            "seller_table",
            "event_table",
            "contract_table",
            "address_table",
            "customer_table",
            "user_table",
        ]
        tables_meta = sorted(Base.metadata.tables.values(), key=lambda table: table.name)

        assert len(tables_models) == len(tables_meta)
        for t in tables_meta:
            assert t.name in tables_models
