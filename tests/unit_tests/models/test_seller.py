import pytest
from datetime import datetime
from sqlalchemy import select
from crm.models.users import Event, Seller
from crm.models.customer import Customer


class TestSeller:
    def test_get_all_clients_of_user(self, db_session, clients, current_user_is_seller):
        # test should return customer list of user (1 customers for this test).
        with db_session as session:
            clients
            current_user = current_user_is_seller
            clients_list = current_user.get_all_clients_of_user(session=session)
            result_excepted = 2
            assert len(clients_list) == result_excepted

    def test_get_all_contracts_of_user(self, db_session, contracts, current_user_is_seller):
        # test should return contracts list of user (1 contract for this test).
        with db_session as session:
            contracts
            current_user = current_user_is_seller
            contracts_list = current_user.get_all_contracts_of_user(session=session)
            result_excepted = 2
            assert len(contracts_list) == result_excepted

    def test_get_unsigned_contracts(self, db_session, contracts, current_user_is_seller):
        # test should return unsigned contracts list (1 contract for this test).
        with db_session as session:
            contracts
            current_user = current_user_is_seller
            unsigned_contracts_list = current_user.get_all_contracts_of_user(session=session)
            result_excepted = 2
            assert len(unsigned_contracts_list) == result_excepted

    def test_get_unpayed_contracts(self, db_session, contracts, current_user_is_seller):
        # test should return unsigned contracts list (1 contract for this test).
        with db_session as session:
            contracts
            current_user = current_user_is_seller
            unpayed_contracts_list = current_user.get_unpayed_contracts(session=session)
            result_excepted = 1
            assert len(unpayed_contracts_list) == result_excepted

    def test_get_all_contract_available_for_event(self, db_session, contracts, current_user_is_seller):
        # Test should return list of contract available for event .
        # Contract should be signed and not linked with event.
        # this contract should be manage by current user.
        with db_session as session:
            contracts
            current_user = current_user_is_seller
            contract_available = current_user.get_all_contracts_of_user_without_event(session=session)
            result_excepted = 1
            assert len(contract_available) == result_excepted

    # ------------- Test Create Functions ---------#

    def test_create_new_customer(self, db_session, clients, current_user_is_seller):
        # test should return a new customer in customers list.
        with db_session as session:
            clients
            current_user = current_user_is_seller
            customer_info = {
                "name": "new_user",
                "email_address": "nw_user@123.com",
                "phone_number": "1235465",
                "company": "the Company",
            }
            new_customer = current_user.create_new_customer(session=session, customer_info=customer_info)
            customer_list = session.scalars(select(Customer)).all()
            assert len(customer_list) == 3
            assert new_customer.seller_contact == current_user

    def test_create_new_event(self, db_session, contracts, address, current_user_is_seller):
        # test should return a new event in event list.
        with db_session as session:
            contract = contracts[0]
            address = address
            current_user = current_user_is_seller
            event_info = {
                "name": "new_event",
                "date_start": datetime.now(),
                "date_end": datetime.now(),
                "attendees": 20,
                "note": "queles notes",
                "contract": contract,
                "supporter": None,
                "address": address,
            }
            new_event = current_user.create_new_event(session=session, event_info=event_info)
            event_list = session.scalars(select(Event)).all()
            assert len(event_list) == 1
            assert new_event.customer == contract.customer

    # ------------- test update-------------- #

    @pytest.mark.parametrize(
        "attribute_update, new_value",
        [("name", "toto"), ("email_address", "234"), ("phone_number", "1616686"), ("company", "the company")],
    )
    def test_update_customers(self, db_session, clients, current_user_is_seller, attribute_update, new_value):
        # Test dhould return a customer updated.
        with db_session as session:
            customer = clients[0]
            current_user = current_user_is_seller
            current_user.update_customer(
                session=session, customer=customer, attribute_update=attribute_update, new_value=new_value
            )
            assert getattr(customer, attribute_update) == new_value
            assert customer.updated_date != None

    @pytest.mark.parametrize(
        "attribute_update, new_value",
        [
            ("created_date", "toto"),
            ("events", "the company"),
            ("contracts", "the company"),
        ],
    )
    def test_update_customer_with_forbidden_atribute_attribute(
        self, db_session, clients, current_user_is_seller, attribute_update, new_value
    ):
        # Test dhould return a customer updated.
        with db_session as session:
            customer = clients[0]
            current_user_is_seller
            Seller().update_customer(
                session=session, customer=customer, attribute_update=attribute_update, new_value=new_value
            )
            assert getattr(customer, attribute_update) != new_value
            assert customer.updated_date == None

    @pytest.mark.parametrize(
        "attribute_update, new_value",
        [("total_amount", 11111111), ("remaining", 0), ("signed_contract", True)],
    )
    def test_update_contract(self, db_session, contracts, current_user_is_seller, attribute_update, new_value):
        # Test dhould return a customer updated.
        with db_session as session:
            contract = contracts[0]
            current_user = current_user_is_seller
            current_user.update_contract(
                session=session, contract=contract, attribute_update=attribute_update, new_value=new_value
            )
            assert getattr(contract, attribute_update) == new_value

    @pytest.mark.parametrize(
        "attribute_update, new_value",
        [
            ("created_date", "toto"),
            ("seller", "234"),
            ("seller_id", "1616686"),
            ("event", "the company"),
            ("customer", "the company"),
            ("customer_id", "the company"),
        ],
    )
    def test_update_contract_with_forbidenn_attribute(
        self, db_session, contracts, current_user_is_seller, attribute_update, new_value
    ):
        # Test dhould return a customer updated.
        with db_session as session:
            contract = contracts[0]
            current_user = current_user_is_seller
            current_user.update_contract(
                session=session, contract=contract, attribute_update=attribute_update, new_value=new_value
            )
            assert getattr(contract, attribute_update) != new_value

    def test_attribute_to_display(self):
        assert Seller().attribute_to_display() == [
            "name",
            "email_address",
            "phone_number",
            "department",
            "created_date",
            "customers",
            "contracts",
        ]
