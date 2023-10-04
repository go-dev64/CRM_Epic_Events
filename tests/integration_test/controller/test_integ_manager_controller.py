import pytest
from sqlalchemy import select
from crm.controller.manager_controller import ManagerController
from crm.models.element_administratif import Contract
from crm.models.users import Manager, Seller, Supporter, User
from crm.models.utils import Utils
import argon2
from rich.console import Console

from crm.view.generic_view import GenericView


class TestManagerController:
    user_info = {
        "name": "toto",
        "email_address": "email@fr",
        "phone_number": "+064849",
        "password": "password",
    }
    info_contract = {"total_amount": 2133333, "remaining": 123, "signed_contract": True}

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

    @pytest.mark.parametrize("department", [(0), (1), (2)])
    def test_create_new_user(self, db_session, users, current_user_is_manager, mocker, department):
        # test should return a new user.
        with db_session as session:
            users
            current_user_is_manager
            manager_ctrl = ManagerController()

            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=department)
            mocker.patch("crm.view.user_view.UserView.get_user_info_view", return_value=self.user_info)
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            number_user_before = self._count_number_of_user(session=session)

            if department == 0:
                user = manager_ctrl.create_new_user(session=session)
                number_user = self._count_number_of_user(session=session)
                assert number_user[0] == number_user_before[0] + 1
                assert number_user[1] == number_user_before[1] + 1
                assert user.name == "toto"
                assert user.email_address == "email@fr"
                assert user.phone_number == "+064849"
                assert user.password == "password"
                mock_confirm.assert_called_once_with(
                    section="Create new collaborator", session=session, msg="Operation succesfull!"
                )

            elif department == 1:
                user = manager_ctrl.create_new_user(session=session)
                number_user = self._count_number_of_user(session=session)
                assert number_user[0] == number_user_before[0] + 1
                assert number_user[2] == number_user_before[2] + 1
                assert user.name == "toto"
                assert user.email_address == "email@fr"
                assert user.phone_number == "+064849"
                assert user.password == "password"
                mock_confirm.assert_called_once_with(
                    section="Create new collaborator", session=session, msg="Operation succesfull!"
                )
            elif department == 2:
                user = manager_ctrl.create_new_user(session=session)
                number_user = self._count_number_of_user(session=session)
                assert number_user[0] == number_user_before[0] + 1
                assert number_user[3] == number_user_before[3] + 1
                assert user.name == "toto"
                assert user.email_address == "email@fr"
                assert user.phone_number == "+064849"
                assert user.password == "password"
                mock_confirm.assert_called_once_with(
                    section="Create new collaborator", session=session, msg="Operation succesfull!"
                )

    @pytest.mark.parametrize("department", [(0), (1), (2)])
    def test_create_new_user_with_no_confirm(self, db_session, users, current_user_is_manager, mocker, department):
        # test should return a new user.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=department)
            mocker.patch("crm.view.user_view.UserView.get_user_info_view", return_value=self.user_info)
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_no_confirm = mocker.patch.object(GenericView, "no_data_message")
            number_user_before = self._count_number_of_user(session=session)
            ManagerController().create_new_user(session=session)
            number_user = self._count_number_of_user(session=session)
            assert number_user_before[0] == number_user[0]
            assert number_user_before[1] == number_user[1]
            assert number_user_before[2] == number_user[2]
            assert number_user_before[3] == number_user[3]
            mock_no_confirm.assert_called_once_with(
                session=session, section="Create new collaborator", msg="Operation Cancelled!"
            )

    def test_select_customer_of_contract(self, db_session, users, clients, current_user_is_manager, mocker):
        # test should return clients of index list 1.
        with db_session as session:
            users
            client = clients[1]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=1)
            result = manager.select_customer_of_contract(session=session)
            assert result == client

    def test_create_new_contract(self, db_session, users, clients, current_user_is_manager, mocker):
        # test should return a new contract.
        with db_session as session:
            users
            client = clients[0]
            current_user_is_manager
            self.info_contract["customer"] = client

            mocker.patch(
                "crm.controller.manager_controller.ManagerController.get_info_contract",
                return_value=self.info_contract,
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            number_of_contract_before = len(session.scalars(select(Contract)).all())
            result = ManagerController().create_new_contract(session=session)
            number_of_contract = len(session.scalars(select(Contract)).all())
            assert number_of_contract == number_of_contract_before + 1
            assert result.total_amount == 2133333
            assert result.remaining == 123
            assert result.signed_contract == True
            assert result.customer == client
            mock_confirm.assert_called_once_with(
                section="Create new Contract", session=session, msg="Operation succesfull!"
            )

    def test_create_new_contract_with_no_comfirm(self, db_session, users, clients, current_user_is_manager, mocker):
        # test should return a msg cncelled and same len of contract list..
        with db_session as session:
            users
            client = clients[0]
            current_user_is_manager
            self.info_contract["customer"] = client
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.get_info_contract",
                return_value=self.info_contract,
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            number_of_contract_before = len(session.scalars(select(Contract)).all())
            ManagerController().create_new_contract(session=session)
            number_of_contract = len(session.scalars(select(Contract)).all())
            assert number_of_contract == number_of_contract_before
            mock_confirm.assert_called_once_with(
                section="Create new Contract", session=session, msg="Operation Cancelled!"
            )

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
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=0)
            if choice == 0:
                assert manager.select_new_department(section="", session=session, collaborator=user) == "Seller"
            elif choice == 1:
                assert manager.select_new_department(session=session, section="", collaborator=user) == "Manager"
            elif choice == 2:
                assert manager.select_new_department(session=session, section="", collaborator=user) == "Manager"

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_collaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a wright user selected.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=users[choice],
            )
            result = ManagerController().select_collaborator(session=session)
            assert result == users[choice]

    def test_change_collaborator_department(self, db_session, users, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_new_department", return_value="Supporter"
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")

            number_before = self._count_number_of_user(session=session)
            ManagerController().change_collaborator_department(session=session, collaborator_selected=users[1])
            number_after = self._count_number_of_user(session=session)
            assert number_after[2] == number_before[2] - 1
            assert number_after[0] == number_before[0]
            assert number_after[3] == number_before[3] + 1
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation succesfull!"
            )

    def test_change_collaborator_department_with_no_confirm(self, db_session, users, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_new_department", return_value="Supporter"
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            number_before = self._count_number_of_user(session=session)
            ManagerController().change_collaborator_department(session=session, collaborator_selected=users[1])
            number_after = self._count_number_of_user(session=session)
            assert number_before == number_after
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation Cancelled!"
            )

    def test_select_customer_of_contract(self, db_session, clients, current_user_is_manager, mocker):
        # test should return customer of index list 1.
        with db_session as session:
            client = clients[1]
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=1)
            result = ManagerController().select_customer_of_contract(session=session)

            assert result == client

    @pytest.mark.parametrize(
        "choice, new_value",
        [
            ("name", "toto"),
            ("email_address", "email@dfkjnekr"),
            ("phone_number", "12351"),
            ("password", "passwrgeord"),
        ],
    )
    def test_change_collaborator_attribute(
        self, db_session, users, current_user_is_manager, mocker, choice, new_value
    ):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            ManagerController().change_collaborator_attribute(
                session=session, collaborator_selected=users[2], attribute_selected=choice
            )
            assert getattr(users[2], choice) == new_value
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation succesfull!"
            )

    @pytest.mark.parametrize("choice", [("name"), ("email_address"), ("phone_number"), ("password")])
    def test_change_collaborator_attribute(self, db_session, users, current_user_is_manager, mocker, choice):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value="new_value")
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            value = getattr(users[2], choice)
            ManagerController().change_collaborator_attribute(
                session=session, collaborator_selected=users[2], attribute_selected=choice
            )
            assert getattr(users[2], choice) == value
            mock_confirm.assert_called_once_with(
                session=session, section=" Update Collaborator", msg="Operation Cancelled!"
            )

    @pytest.mark.parametrize(
        "old_attribute, new_value",
        [("total_amount", 123), ("remaining", 12), ("signed_contract", True)],
    )
    def test_update_contract(
        self, db_session, users, current_user_is_manager, contracts, mocker, old_attribute, new_value
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
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            manager.update_contract(session=session)
            if old_attribute == "total_amount":
                assert getattr(contract, old_attribute) == new_value
            elif old_attribute == "remaining":
                assert getattr(contract, old_attribute) == new_value
            elif old_attribute == "signed_contract":
                assert getattr(contract, old_attribute) == new_value

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
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)

            if choice == 0:
                assert manager.select_supporter(session=session) == users[2]
            elif choice == 1:
                assert manager.select_supporter(session=session) == supporter_2

    def test_delete_collaborator(self, db_session, users, current_user_is_manager, mocker):
        # Test should retrun a user less one.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=users[1],
            )

            manager.delete_collaborator(session=session)
            user_list = session.scalars(select(User)).all()
            seller_list = session.scalars(select(Seller)).all()
            assert len(user_list) == 2
            assert len(seller_list) == 0

    def test_update_collaborator_with_department(self, db_session, users, current_user_is_manager, mocker):
        # test should return a updated attribute of user selected.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=users[1],
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_new_department",
                return_value="Supporter",
            )
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value="department",
            )
            ManagerController().update_collaborator(session=session)
            user_list = session.scalars(select(User)).all()
            seller_list = session.scalars(select(Supporter)).all()
            assert len(user_list) == 3
            assert len(seller_list) == 2

    def test_update_collaborator_with_password(self, db_session, users, current_user_is_manager, mocker):
        # test should return a updated attribute of user selected.
        with db_session as session:
            user = users[1]
            current_user_is_manager
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=user,
            )
            mocker.patch(
                "rich.prompt.Prompt.ask",
                return_value="Abcdefgh@45",
            )
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value="password",
            )
            ph = argon2.PasswordHasher()
            ManagerController().update_collaborator(session=session)
            assert ph.verify(user.password, "Abcdefgh@45") == True
