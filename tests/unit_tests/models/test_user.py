from datetime import datetime
import pytest
from sqlalchemy import select
from crm.models.users import Manager, Seller, Supporter, Address, User
from crm.models.customer import Customer


client = Customer(name="client_1", email_address="clien_1@123.com", phone_number="123456", company="7eme_company")


class TestUser:
    def test_get_all_clients(self, db_session, clients, current_user_is_user):
        # test should return list of clients.
        with db_session as session:
            clients
            current_user = current_user_is_user
            session.current_user = current_user
            customers_list = current_user.get_all_customers(session=session)
            result_excepted = 2
            assert len(customers_list) == result_excepted

    def test_get_all_contracts(self, db_session, contracts, current_user_is_user):
        # test should return list of contracts.
        with db_session as session:
            contracts
            current_user = current_user_is_user
            session.current_user = current_user
            contract_list = current_user.get_all_contracts(session=session)
            result_excepted = 2
            assert len(contract_list) == result_excepted

    def test_get_all_events(self, db_session, events, current_user_is_user):
        # test should return list of events.
        with db_session as session:
            events
            current_user = current_user_is_user
            session.current_user = current_user
            events_list = current_user.get_all_events(session=session)
            result_excepted = 2
            assert len(events_list) == result_excepted

    def test_create_new_address(self, db_session, users, address, current_user_is_user):
        # test should return a new address in address list.
        with db_session as session:
            users
            address = address
            current_user = current_user_is_user
            address_info = {
                "number": 12,
                "street": "street",
                "city": "city",
                "postal_code": 45398,
                "country": "france",
                "note": "une note",
            }
            new_address = current_user.create_new_address(session=session, address_info=address_info)
            address_list = session.scalars(select(Address)).all()
            result_excepted = 2
            assert len(address_list) == result_excepted

    def test_attribute_to_display(self):
        assert User().attribute_to_display() == [
            {"attribute_name": "name"},
            {"attribute_name": "email_address"},
            {"attribute_name": "phone_number"},
            {"attribute_name": "created_date"},
            {"attribute_name": "department"},
        ]

    def test_availables_attribue_list(self):
        assert User().availables_attribue_list() == [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 10}},
            {"attribute_name": "password", "parametre": {"type": str, "max": None}},
            {"attribute_name": "department", "parametre": {"type": object, "max": None}},
        ]
