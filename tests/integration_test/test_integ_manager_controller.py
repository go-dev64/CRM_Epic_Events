import pytest
from sqlalchemy import select
from crm.controller.manager_controller import ManagerController
from crm.models.element_administratif import Contract
from crm.models.users import Manager, Seller, Supporter, User
from crm.models.utils import Utils


class TestManagerController:
    @pytest.mark.parametrize("department", [(1), (2), (3)])
    def test_create_new_user(self, db_session, users, current_user_is_manager, mocker, department):
        # test should return a new user.
        with db_session as session:
            users
            current_user_is_manager
            manager_ctrl = ManagerController()
            user_info = {
                "name": "toto",
                "email_address": "email@fr",
                "phone_number": "+064849",
                "password": "password",
            }
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=department)
            mocker.patch("crm.view.user_view.UserView.get_user_info_view", return_value=user_info)

            if department == 1:
                new_user = manager_ctrl.create_new_user(session=session)
                list_manager = session.scalars(select(Manager)).all()
                list_user = session.scalars(select(User)).all()
                assert len(list_manager) == 2
                assert len(list_user) == 4

            elif department == 2:
                new_user = manager_ctrl.create_new_user(session=session)
                list_seller = session.scalars(select(Seller)).all()
                list_user = session.scalars(select(User)).all()
                assert len(list_seller) == 2
                assert len(list_user) == 4
            elif department == 3:
                new_user = manager_ctrl.create_new_user(session=session)
                list_supporter = session.scalars(select(Supporter)).all()
                list_user = session.scalars(select(User)).all()
                assert len(list_supporter) == 2
                assert len(list_user) == 4

    def test_create_new_contract(self, db_session, users, clients, contracts, current_user_is_manager, mocker):
        # test should return a new contract.
        with db_session as session:
            contracts
            current_user_is_manager
            manager_ctrl = ManagerController()
            contract_info = {
                "total_amount": 1000,
                "remaining": 0,
                "signed_contract": True,
                "customer": clients[0],
                "seller": users[1],
            }
            mocker.patch("crm.view.contract_view.ContractView.get_info_contract", return_value=contract_info)
            new_contract = manager_ctrl.create_new_contract(session=session)
            list_contract = session.scalars(select(Contract)).all()
            assert len(list_contract) == 3

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test__get_departement_list(self, db_session, users, current_user_is_manager, choice):
        # test should return the available department list.
        with db_session as session:
            user = users[choice]
            current_user_is_manager
            manager = ManagerController()
            if choice == 0:
                assert manager._get_department_list(user) == ["Seller", "Supporter"]
            elif choice == 1:
                assert manager._get_department_list(user) == ["Manager", "Supporter"]
            elif choice == 2:
                assert manager._get_department_list(user) == ["Manager", "Seller"]

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test__select_new_department(self, db_session, users, current_user_is_manager, choice, mocker):
        # according ti user's choice, test should return a good department in list choice.
        with db_session as session:
            user = users[choice]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=0)
            if choice == 0:
                assert manager._select_new_department(user) == "Seller"
            elif choice == 1:
                assert manager._select_new_department(user) == "Manager"
            elif choice == 2:
                assert manager._select_new_department(user) == "Manager"

    @pytest.mark.parametrize(
        "old_attribute, new_value",
        [("total_amount", 123), ("remaining", 12), ("signed_contract", True)],
    )
    def test_update_contract(
        self, db_session, users, current_user_is_manager, contracts, clients, mocker, old_attribute, new_value
    ):
        with db_session as session:
            users
            current_user_is_manager
            contract = contracts[0]
            manager = ManagerController()
            mocker.patch("crm.models.utils.Utils._select_element_in_list", return_value=contract)
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value=old_attribute,
            )
            mocker.patch("crm.models.utils.Utils._get_new_value_of_attribut", return_value=new_value)
            manager.update_contract(session=session)
            if old_attribute == "total_amount":
                assert getattr(contract, old_attribute) == new_value
            elif old_attribute == "remaining":
                assert getattr(contract, old_attribute) == new_value
            elif old_attribute == "signed_contract":
                assert getattr(contract, old_attribute) == new_value

    def test_update_contract_to_customer_attribute(
        self, db_session, users, current_user_is_manager, contracts, clients, mocker
    ):
        with db_session as session:
            users
            current_user_is_manager
            client = clients[0]
            contract = contracts[0]
            manager = ManagerController()
            mocker.patch("crm.models.utils.Utils._select_element_in_list", return_value=contract)
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value="customer",
            )
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=client,
            )
            manager.update_contract(session=session)
            assert contract.customer == client

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test__select_supporter(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return the good element of list according to user's choice.
        with db_session as session:
            users
            supporter_2 = Supporter(
                name="supporter_2", email_address="email_supporter2", phone_number="023153", password="35516"
            )
            session.add(supporter_2)
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)

            if choice == 0:
                assert manager._select_supporter(session=session) == users[2]
            elif choice == 1:
                assert manager._select_supporter(session=session) == supporter_2
