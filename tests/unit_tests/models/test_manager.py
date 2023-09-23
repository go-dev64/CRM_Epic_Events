import pytest
from sqlalchemy import select
from crm.models.users import Manager, Seller, Supporter, User, Contract


user_info = {
    "name": "new_user",
    "email_address": "nw_user@123.com",
    "phone_number": "1235465",
    "password": "password",
}


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

    def test_get_all_supporter(self, db_session, users, current_user_is_manager):
        # test should return list of Supporter.
        with db_session as session:
            users
            current_user = current_user_is_manager
            supporter_list = current_user.get_all_supporter(session=session)
            result_excepted = 2
            assert len(supporter_list) == result_excepted

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
            contract_info = {"total_amount": 1000, "remaining": 500, "signed_contract": True, "customer": client}
            result_accepted = 1
            contract = current_user.create_new_contract(session=session, contract_info=contract_info)
            contract_list = session.scalars(select(Contract)).all()

            assert len(contract_list) == result_accepted
            assert contract.seller == client.seller_contact

    # -------------- test of update --------------------- #

    def test_update_user(self, db_session, users, current_user_is_manager):
        # Test should update a  attribut of user.
        with db_session as session:
            user = users[1]
            current_user = current_user_is_manager
            update_attribute = "name"
            new_value = "toto"
            current_user.update_user(
                session=session, collaborator=user, update_attribute=update_attribute, new_value=new_value
            )
            test = session.scalars(select(User).where(User.id == user.id)).all()
            assert test[0].name == new_value

    @pytest.mark.parametrize(
        "new_department, new_class_department, old_department",
        [("manager", Manager, 1), ("seller", Seller, 2), ("supporter", Supporter, 0)],
    )
    def test_update_departement(
        self, db_session, users, current_user_is_manager, new_department, new_class_department, old_department
    ):
        # Test should change a user of department. Nomber user is same.
        # The number of user per department changes = 2.

        with db_session as session:
            user = users[old_department]
            id = user.id
            current_user = current_user_is_manager

            new_user = current_user.change_user_department(
                session=session, collaborator=user, new_department=new_department
            )

            list_of_department = session.scalars(select(new_class_department)).all()
            list_user = session.scalars(select(User)).all()

            assert len(list_of_department) == 2
            assert len(list_user) == 3

    def test_update_contract_with_change_customer(self, db_session, contracts, clients, current_user_is_manager):
        # Test should return a updated contract with a same seller for customer and contract.
        with db_session as session:
            contract = contracts[0]
            client = clients[0]
            current_user = current_user_is_manager
            seller2 = Seller(name="seller_2", email_address="hhh@", password="password")
            session.add(seller2)
            client.seller_contact = seller2
            contract.customer = client
            current_user.update_contract(
                session=session, contract=contract, attribute_update="customer", new_value=client
            )
            assert contract.seller_id == contract.customer.seller_contact_id

    @pytest.mark.parametrize(
        "attribute_update, new_value", [("total_amont", 500000), ("remaining", 100), ("signed_contract", True)]
    )
    def test_update_contract(self, db_session, contracts, current_user_is_manager, attribute_update, new_value):
        # Test should return a updated contract.
        with db_session as session:
            contract = contracts[0]
            current_user = current_user_is_manager
            current_user.update_contract(
                session=session, contract=contract, attribute_update=attribute_update, new_value=new_value
            )
            assert getattr(contract, attribute_update) == new_value

    def test_change_supporter_of_event(self, db_session, events, current_user_is_manager):
        # Test should return a event with a new supporter.
        with db_session as session:
            event = events[0]
            supporter = session.scalars(select(Supporter)).first()
            assert event.supporter == None
            current_user = current_user_is_manager
            current_user.change_supporter_of_event(session=session, event=event, new_supporter=supporter)
            assert getattr(event, "supporter") == supporter

    def test_update_seller_contact_of_customer(self, db_session, clients, contracts, current_user_is_manager):
        # Test should return a updated contract.
        with db_session as session:
            client = clients[0]
            contract = contracts[0]
            current_user = current_user_is_manager
            seller2 = Seller(name="seller_2", email_address="hhh@", password="password")
            session.add(seller2)
            current_user.update_seller_contact_of_customer(session=session, customer=client, new_seller=seller2)
            assert client.seller_contact == seller2
            assert contract.seller == client.seller_contact

    # --------------- delete test ------------- #

    @pytest.mark.parametrize("user_has_delete", [(0), (1), (2)])
    def test_delete_collaborator(self, db_session, users, events, current_user_is_manager, user_has_delete):
        # test should delete 1 user.
        with db_session as session:
            user = users[user_has_delete]
            events
            current_user = current_user_is_manager
            current_user.delete_collaborator(session=session, collaborator_has_delete=user)
            list_user = session.scalars(select(User)).all()
            assert len(list_user) == 2
