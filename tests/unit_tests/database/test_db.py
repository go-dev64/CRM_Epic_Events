import pytest
from sqlalchemy import text
from crm.database.controller.db_controller import Database
from crm.models.base import Base
import crm.models.users
import crm.models.customer
import crm.models.element_administratif
from tests.factory.user_factory import Manager

db = Database()


class TestDatabase:
    def test_database_connection(self, connection):
        # test try to connect to database
        try:
            assert connection is not None
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

    def test_check_add_user(self, db_session):
        with db_session as session:
            user = Manager(name="toto", email_address="toto@gmail.com", phone_number="+0335651", password="toto")
            session.add_all([user])

            assert session.query(Manager).one()

            session.rollback()

    def test_create_table(self, db_session):
        tables_models = [
            "supporter_table",
            "manager_table",
            "seller_table",
            "event_table",
            "contract_table",
            "address_table",
            "customer_table",
        ]
        with db_session as session:
            for table in tables_models:
                texte = text(f"SELECT * from {table};")
                data = session.execute(texte).all()
                assert data == []
