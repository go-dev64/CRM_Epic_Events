import pytest
from crm_app.crm.models.customer import Customer

client = Customer(name="client_1", email_address="clien_1@123.com", phone_number="123456", company="7eme_company")


class TestUser:
    def _create_users(self, session, users):
        # Create users for test.
        session.add_all(users)
        session.commit()

    def _create_clients(self, session, clients):
        session.add(clients)
        session.commit()

    def _create_contracts(self, session, contracts):
        session.add(contracts)
        session.commit()

    def test_get_all_clients(self, db_session, users):
        self._create_users(db_session, users)
