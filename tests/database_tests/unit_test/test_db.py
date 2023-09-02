import pytest
from sqlalchemy import text
from crm_app.database.models.db_controller import Database
from crm_app.user.models.base import Base
import crm_app.user.models.users
import crm_app.crm.models.customer
import crm_app.crm.models.element_administratif
from tests.factory.user_factory import Manager, ManagerFactory

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
            "company_table",
            "customer_table",
        ]
        tables_meta = sorted(Base.metadata.tables.values(), key=lambda table: table.name)
        assert len(tables_models) == len(tables_meta)
        for t in tables_meta:
            assert t.name in tables_models

    def test_create_manager(self):
        pass

    def test_create_seller(self):
        pass

    def test_create_supporter(self):
        pass

    def test_toto(self, mocked_session):
        with mocked_session as session:
            user = Manager(name="toto", email_address="toto@gmail.com", phone_number="+0335651", password="toto")
            session.add_all([user])

            assert session.query(Manager).one()

            session.rollback()

    def test_create_table(self, mocked_session):
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
        for table in tables_models:
            texte = text(f"SELECT * from {table};")
            data = mocked_session.execute(texte).all()
            assert data == []
