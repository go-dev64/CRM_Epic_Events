import pytest
from sqlalchemy import select
from crm.models.customer import Customer
from crm.models.element_administratif import Address, Event
from crm.models.users import Manager, Seller, Supporter, User, Contract


user_info = {
    "name": "new_user",
    "email_address": "nw_user@123.com",
    "phone_number": "1235465",
    "password": "password",
}


class TestManager:
    def _count_number_of_element(self, session) -> tuple():
        """the function count number of element in session.

        Args:
            session (_type_): _description_

        Returns:
            tuple(int,int,int,int): number_customer, number_contract, number_event, number_address
        """
        number_contract = len(session.scalars(select(Contract)).all())
        number_customer = len(session.scalars(select(Customer)).all())
        number_event = len(session.scalars(select(Event)).all())
        number_address = len(session.scalars(select(Address)).all())
        return number_customer, number_contract, number_event, number_address

    def _count_number_of_user(self, session) -> tuple:
        """the function count number of users in session.

        Args:
            session (_type_): _description_

        Returns:
            tuple: (number_user, number_manager, number_seller, number_supporter)
        """
        number_manager = len(session.scalars(select(Manager)).all())
        number_seller = len(session.scalars(select(Seller)).all())
        number_supporter = len(session.scalars(select(Supporter)).all())
        number_user = len(session.scalars(select(User)).all())
        return number_user, number_manager, number_seller, number_supporter

    """
    READ test function
    """

    def test_get_all_user(self, db_session, users, current_user_is_manager):
        # test should return list of events.
        with db_session as session:
            users
            current_user = current_user_is_manager
            users_list = current_user.get_all_users(session=session)
            result_excepted = self._count_number_of_user(session)[0]
            assert len(users_list) == result_excepted

    def test_get_all_supporter(self, db_session, users, current_user_is_manager):
        # test should return list of Supporter.
        with db_session as session:
            users
            current_user = current_user_is_manager
            supporter_list = current_user.get_all_supporter(session=session)
            result_excepted = self._count_number_of_user(session)[3]
            assert len(supporter_list) == result_excepted

    def test_get_all_event_without_support(self, db_session, events, current_user_is_manager):
        # test
        with db_session as session:
            events
            current_user_is_manager
            events_list = Manager().get_all_event_without_support(session=session)
            result_excepted = len(session.scalars(select(Event).where(Event.supporter == None)).all())
            assert result_excepted == len(events_list)

    def test_get_customer_without_seller(sel, db_session, users, clients, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            clients
            clients[0].seller_contact = None
            result = Manager().get_customer_without_seller(session=session)
            for r in result:
                assert isinstance(r, Customer)
                assert r.seller_contact == None

    # ------------- Test Create Functions ---------#

    def test_add_new_manager(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new manager in manager list
        with db_session as session:
            users
            current_user = current_user_is_manager
            list_user_before = self._count_number_of_user(session)[0]
            list_manager_before = self._count_number_of_user(session)[1]
            new_manager = current_user.create_new_manager(session=session, user_info=user_info)
            list_user = self._count_number_of_user(session)[0]
            list_manager = self._count_number_of_user(session)[1]

            assert list_user_before + 1 == list_user
            assert list_manager_before + 1 == list_manager

    def test_add_new_seller(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            list_user_before = self._count_number_of_user(session)[0]
            list_seller_before = self._count_number_of_user(session)[2]
            new_seller = current_user.create_new_seller(session=session, user_info=user_info)
            list_user = self._count_number_of_user(session)[0]
            list_seller = self._count_number_of_user(session)[2]

            assert list_user == list_user_before + 1
            assert list_seller == list_seller_before + 1

    def test_add_new_supporter(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            list_user_before = self._count_number_of_user(session)[0]
            list_supporter_before = self._count_number_of_user(session)[3]

            new_supporter = current_user.create_new_supporter(session=session, user_info=user_info)
            list_user = self._count_number_of_user(session)[0]
            list_supporter = self._count_number_of_user(session)[3]

            assert list_user == list_user_before + 1
            assert list_supporter == list_supporter_before + 1

    def test_add_new_user_with_wrong_data(self, db_session, users, current_user_is_manager):
        # Test should return a new user in list user(len = 4) and new seller in seller list.
        with db_session as session:
            users
            current_user = current_user_is_manager
            bad_user_info = {
                "name": "new_user",
                "phone_number": "1235465",
                "password": "password",
            }
            list_user_before = self._count_number_of_user(session)[0]
            new_supporter = current_user.create_new_supporter(session=session, user_info=bad_user_info)
            list_user = self._count_number_of_user(session)[0]
            assert list_user == list_user_before
            assert new_supporter == None

    def test_create_new_contract(self, db_session, clients, current_user_is_manager):
        # Test should return a new contract in contracts list.
        with db_session as session:
            client = clients[0]
            current_user = current_user_is_manager
            contract_info = {"total_amount": 1000, "remaining": 500, "signed_contract": True, "customer": client}
            contract_list_before = self._count_number_of_element(session)[1]
            contract = current_user.create_new_contract(session=session, contract_info=contract_info)
            contract_list = self._count_number_of_element(session)[1]

            assert contract_list == contract_list_before + 1
            assert contract.seller == client.seller_contact

    # -------------- test of update --------------------- #

    def test_update_user(self, db_session, users, current_user_is_manager):
        # Test should update a  attribut of user.
        with db_session as session:
            user = users[1]
            current_user = current_user_is_manager
            update_attribute = "name"
            new_value = "toto"
            Manager().update_user(collaborator=user, update_attribute=update_attribute, new_value=new_value)
            test = session.scalars(select(User).where(User.id == user.id)).all()
            assert test[0].name == new_value

    @pytest.mark.parametrize(
        "new_department, new_class_department, old_department",
        [("Manager", Manager, 1), ("Seller", Seller, 2), ("Supporter", Supporter, 0)],
    )
    def test_update_departement(
        self, db_session, users, current_user_is_manager, new_department, new_class_department, old_department
    ):
        # Test should change a user of department. Nomber user is same.
        # number of new department +1.

        with db_session as session:
            user = users[old_department]
            id = user.id
            current_user = current_user_is_manager
            list_user_before = self._count_number_of_user(session)[0]
            list_of_department_before = len(session.scalars(select(new_class_department)).all())
            new_user = Manager().change_user_department(
                session=session, collaborator=user, new_department=new_department
            )
            list_user = self._count_number_of_user(session)[0]
            list_of_department = len(session.scalars(select(new_class_department)).all())
            assert list_of_department == list_of_department_before + 1
            assert list_user == list_user_before

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
            current_user.update_contract(contract=contract, attribute_update="customer", new_value=client)
            assert contract.seller_id == contract.customer.seller_contact_id

    @pytest.mark.parametrize(
        "attribute_update, new_value", [("total_amont", 500000), ("remaining", 100), ("signed_contract", True)]
    )
    def test_update_contract(self, db_session, contracts, current_user_is_manager, attribute_update, new_value):
        # Test should return a updated contract.
        with db_session as session:
            contract = contracts[0]
            current_user = current_user_is_manager
            current_user.update_contract(contract=contract, attribute_update=attribute_update, new_value=new_value)
            assert getattr(contract, attribute_update) == new_value

    def test_change_supporter_of_event(self, db_session, events, current_user_is_manager):
        # Test should return a event with a new supporter.
        with db_session as session:
            event = events[0]
            supporter = session.scalars(select(Supporter)).first()
            assert event.supporter == None
            current_user = current_user_is_manager
            Manager().change_supporter_of_event(session=session, event=event, new_supporter=supporter)
            assert getattr(event, "supporter") == supporter

    def test_update_seller_contact_of_customer(self, db_session, clients, contracts, current_user_is_manager):
        # Test should return a updated contract.
        with db_session as session:
            client = clients[0]
            contract = contracts[0]
            current_user = current_user_is_manager
            seller2 = Seller(name="seller_2", email_address="hhh@", password="password")
            session.add(seller2)
            Manager().update_seller_contact_of_customer(customer=client, new_seller=seller2)
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
            list_user_before = self._count_number_of_user(session)[0]
            current_user.delete_collaborator(session=session, collaborator_has_delete=user)
            list_user = self._count_number_of_user(session)[0]
            assert list_user == list_user_before - 1
