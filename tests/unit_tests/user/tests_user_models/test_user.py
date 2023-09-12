import pytest
from sqlalchemy import select
from crm_app.crm.models.element_administratif import Contract
from crm_app.user.models.users import Manager, Seller, Supporter, User, Authentication
from crm_app.crm.models.customer import Customer


client = Customer(name="client_1", email_address="clien_1@123.com", phone_number="123456", company="7eme_company")

user_info = {
    "name": "new_user",
    "email_address": "nw_user@123.com",
    "phone_number": "1235465",
    "password": "password",
}


class TestUserRead:
    def _user__current(self, session, user_type):
        user = session.scalars(select(user_type)).first()
        user = Authentication.get_token(user)
        return user

    @pytest.mark.parametrize("type_user", [(Manager), (Seller), (Supporter)])
    def test_get_all_clients(self, db_session, clients, type_user):
        # test should return list of clients.
        with db_session as session:
            clients
            current_user = self._user__current(session, type_user)
            session.current_user = current_user
            customers_list = current_user.get_all_customers(session=session)
            result_excepted = 2
            assert len(customers_list) == result_excepted

    @pytest.mark.parametrize("type_user", [(Manager), (Seller), (Supporter)])
    def test_get_all_contracts(self, db_session, contracts, type_user):
        # test should return list of contracts.
        with db_session as session:
            contracts
            current_user = self._user__current(session, type_user)
            session.current_user = current_user
            contract_list = current_user.get_all_contracts(session=session)
            result_excepted = 2
            assert len(contract_list) == result_excepted

    @pytest.mark.parametrize("type_user", [(Manager), (Seller), (Supporter)])
    def test_get_all_events(self, db_session, events, type_user):
        # test should return list of events.
        with db_session as session:
            events
            current_user = self._user__current(session, type_user)
            session.current_user = current_user
            events_list = current_user.get_all_events(session=session)
            result_excepted = 2
            assert len(events_list) == result_excepted


class TestManager:
    """
    READ test function
    """

    def test_get_all_user(self, db_session, users, current_user_is_manager):
        # test should return list of events.
        with db_session as session:
            users
            current_user = current_user_is_manager
            users_list = current_user.get_all_users(session=session)
            result_excepted = 3
            assert len(users_list) == result_excepted

    def test_get_all_event_without_support(self, db_session, events, current_user_is_manager):
        # test
        with db_session as session:
            events
            current_user = current_user_is_manager
            events_list = current_user.get_all_event_without_support(session=session)
            result_excepted = 1
            assert result_excepted == len(events_list)

    # ------------- Test Create Functions ---------#

    def test_add_new_manager(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new manager in manager list
        with db_session as session:
            users
            current_user = current_user_is_manager
            result_accepted = 4
            new_manager = current_user.create_new_manager(session=session, user_info=user_info)
            list_user = session.scalars(select(User)).all()
            list_manager = session.scalars(select(Manager)).all()

            assert len(list_user) == result_accepted
            assert len(list_manager) == 2

    def test_add_new_seller(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            result_accepted = 4
            new_seller = current_user.create_new_seller(session=session, user_info=user_info)
            list_user = session.scalars(select(User)).all()
            list_seller = session.scalars(select(Seller)).all()

            assert len(list_user) == result_accepted
            assert len(list_seller) == 2

    def test_add_new_seller(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            result_accepted = 4
            new_seller = current_user.create_new_seller(session=session, user_info=user_info)
            list_user = session.scalars(select(User)).all()
            list_seller = session.scalars(select(Seller)).all()

            assert len(list_user) == result_accepted
            assert len(list_seller) == 2

    def test_add_new_supporter(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            result_accepted = 4
            new_supporter = current_user.create_new_supporter(session=session, user_info=user_info)
            list_user = session.scalars(select(User)).all()
            list_supporter = session.scalars(select(Supporter)).all()

            assert len(list_user) == result_accepted
            assert len(list_supporter) == 2

    def test_add_new_user_with_wrong_data(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            result_accepted = 3
            bad_user_info = {
                "name": "new_user",
                "phone_number": "1235465",
                "password": "password",
            }
            new_supporter = current_user.create_new_supporter(session=session, user_info=bad_user_info)
            list_user = session.scalars(select(User)).all()

            assert len(list_user) == result_accepted
            assert new_supporter == None

    def test_create_new_contract(self, db_session, clients, current_user_is_manager):
        # Test should return a new contract in contracts list.
        with db_session as session:
            client = clients[0]
            current_user = current_user_is_manager
            contract_info = {"total_amount": 1000, "remaining": 500, "signed_contract": True, "customer_id": client.id}
            result_accepted = 1
            contract = current_user.create_new_contract(session=session, contract_info=contract_info)
            list_user = session.scalars(select(Contract)).all()
            assert len(list_user) == result_accepted


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


class TestSupporter:
    def _user__current(self, session, user_type):
        user = session.scalars(select(user_type)).first()
        user = Authentication.get_token(user)
        session.current_user = user

    def test_get_event_of_supporter(self, db_session, events, current_user_is_supporter):
        # test should return events list without supporter.

        with db_session as session:
            events
            current_user = current_user_is_supporter
            event_list_of_user = current_user.get_event_of_supporter(session=session)
            result_excepted = 1
            assert len(event_list_of_user) == result_excepted
