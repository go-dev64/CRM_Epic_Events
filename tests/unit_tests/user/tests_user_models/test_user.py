import pytest
from sqlalchemy import select
from crm_app.user.models.users import Manager, Seller, Supporter, User, Authentication
from crm_app.crm.models.customer import Customer


client = Customer(name="client_1", email_address="clien_1@123.com", phone_number="123456", company="7eme_company")


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

    def _user__current(self, session, user_type):
        user = session.scalars(select(user_type)).first()
        user = Authentication.get_token(user)
        session.current_user = user

    def test_get_all_user(self, db_session, users):
        # test should return list of events.
        with db_session as session:
            users
            self._user__current(session, Manager)
            users_list = session.current_user.get_all_users(session=session)
            result_excepted = 3
            assert len(users_list) == result_excepted

    def test_get_all_event_without_support(self, db_session, events):
        # test
        with db_session as session:
            events
            self._user__current(session, Manager)
            events_list = session.current_user.get_all_event_without_support(session=session)
            result_excepted = 1
            assert result_excepted == len(events_list)

    # ------------- Test Create Functions ---------#

    def test_add_new_user(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4).
        with db_session as session:
            users
            current_user = current_user_is_manager
            result_accepted = 4
            user_info = {
                "name": "new_user",
                "email_address": "nw_user@123.com",
                "phone_number": "1235465",
                "password": "password",
            }
            new_user = current_user.create_new_user(session=session, user_info=user_info)
            list_user = session.scalars(select(User)).all()
            assert len(list_user) == result_accepted


class TestSeller:
    def _user__current(self, session, user_type):
        user = session.scalars(select(user_type)).first()
        user = Authentication.get_token(user)
        session.current_user = user

    def test_get_all_clients_of_user(self, db_session, clients):
        # test should return customer list of user (1 customers for this test).
        with db_session as session:
            clients
            self._user__current(session, Seller)
            clients_list = session.current_user.get_all_clients_of_user(session=session)
            result_excepted = 2
            assert len(clients_list) == result_excepted

    def test_get_all_contracts_of_user(self, db_session, contracts):
        # test should return contracts list of user (1 contract for this test).
        with db_session as session:
            contracts
            self._user__current(session, Seller)
            contracts_list = session.current_user.get_all_contracts_of_user(session=session)
            result_excepted = 2
            assert len(contracts_list) == result_excepted

    def test_get_unsigned_contracts(self, db_session, contracts):
        # test should return unsigned contracts list (1 contract for this test).
        with db_session as session:
            contracts
            self._user__current(session, Seller)
            unsigned_contracts_list = session.current_user.get_all_contracts_of_user(session=session)
            result_excepted = 2
            assert len(unsigned_contracts_list) == result_excepted

    def test_get_unpayed_contracts(self, db_session, contracts):
        # test should return unsigned contracts list (1 contract for this test).
        with db_session as session:
            contracts
            self._user__current(session, Seller)
            unpayed_contracts_list = session.current_user.get_unpayed_contracts(session=session)
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
