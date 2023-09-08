import pytest
from sqlalchemy import select
from crm_app.user.models.users import Manager, Seller, Supporter, User
from crm_app.crm.models.customer import Customer

client = Customer(name="client_1", email_address="clien_1@123.com", phone_number="123456", company="7eme_company")


class TestUser:
    def _create_users(self, session, users):
        # Create users for test.
        session.add_all(users)
        session.commit()

    def _create_clients(self, session, client):
        session.add(client)
        session.commit()

    def _create_contracts(self, session, contracts):
        session.add(contracts)
        session.commit()

    def test_get_all_clients(self, db_session, users):
        with db_session as session:
            self._create_users(session, users)
            self._create_clients(session, client)
            customers_list = User.get_customers()

            customers_excepted = session.scalars(select(Customer)).all()
            assert customers_list == customers_excepted
