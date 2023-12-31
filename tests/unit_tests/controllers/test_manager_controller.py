import pytest
from sqlalchemy import select
from crm.controller.manager_controller import ManagerController
from crm.models.users import Manager, Seller, Supporter, User
from crm.models.utils import Utils
from crm.view.generic_view import GenericView


class TestManagerController:
    def _count_number_of_user(self, session):
        number_manager = len(session.scalars(select(Manager)).all())
        number_seller = len(session.scalars(select(Seller)).all())
        number_supporter = len(session.scalars(select(Supporter)).all())
        number_user = len(session.scalars(select(User)).all())
        return number_user, number_manager, number_seller, number_supporter

    info_contract = {"total_amount": 2133333, "remaining": 123, "signed_contract": True}

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test_create_new_element(self, db_session, users, current_user_is_manager, mocker, choice):
        # test check if the wright function is returned according to user's choise.
        with db_session as session:
            users
            current_user_is_manager
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 3]
            mock_user = mocker.patch.object(ManagerController, "create_new_user")
            mock_contract = mocker.patch.object(ManagerController, "create_new_contract")
            mock_address = mocker.patch.object(Utils, "create_new_address")

            ManagerController().create_new_element(session=session)
            if choice == 0:
                mock_user.assert_called_once()
            elif choice == 1:
                mock_contract.assert_called_once()
            elif choice == 2:
                mock_address.assert_called_once()

    @pytest.mark.parametrize("department", [(0), (1), (2)])
    def test_create_new_user(self, db_session, users, current_user_is_manager, mocker, department):
        # test should return a good function of creating user according to user's choice..
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=department)
            mocker.patch("crm.view.user_view.UserView.get_user_info_view")
            mock_new_manager = mocker.patch.object(Manager, "create_new_manager")
            mock_new_seller = mocker.patch.object(Manager, "create_new_seller")
            mock_new_supporter = mocker.patch.object(Manager, "create_new_supporter")
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            ManagerController().create_new_user(session=session)
            if department == 0:
                mock_new_manager.assert_called_once()
                mock_confirm.assert_called_once_with(
                    section="Create new collaborator", session=session, msg="Operation succesfull!"
                )
            elif department == 1:
                mock_new_seller.assert_called_once()
                mock_confirm.assert_called_once_with(
                    section="Create new collaborator", session=session, msg="Operation succesfull!"
                )

            elif department == 2:
                mock_new_supporter.assert_called_once()
                mock_confirm.assert_called_once_with(
                    section="Create new collaborator", session=session, msg="Operation succesfull!"
                )

    @pytest.mark.parametrize("department", [(0), (1), (2)])
    def test_create_new_user_with_no_confirm(self, db_session, users, current_user_is_manager, mocker, department):
        # test should return a good function of creating user according to user's choice..
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=department)
            mocker.patch("crm.view.user_view.UserView.get_user_info_view")
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_no_confirm = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().create_new_user(session=session)
            mock_no_confirm.assert_called_once_with(
                session=session, section="Create new collaborator", msg="Operation Cancelled!"
            )

    def test_get_contract_info(self, db_session, clients, current_user_is_manager, mocker):
        # test should return a info of contract.
        with db_session as session:
            clients
            current_user_is_manager
            info_contract = {
                "total_amount": 2133333,
                "remaining": 123,
                "signed_contract": True,
                "customer": clients[0],
            }
            mocker.patch("crm.view.manager_view.ManagerView.get_info_contract_view", return_value=info_contract)
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_customer_of_contract", return_value=""
            )
            result = ManagerController().get_info_contract(session=session)
            assert result == info_contract

    def test_select_customer_of_contract(self, db_session, users, current_user_is_manager, mocker):
        # test should return element of index list 1.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_all_customers", return_value=element_list)
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=1)
            result = manager.select_customer_of_contract(session=session)
            assert result == element_list[1]

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
            mock_contract = mocker.patch.object(Manager, "create_new_contract")
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            ManagerController().create_new_contract(session=session)
            mock_contract.assert_called_once_with(session=session, contract_info=self.info_contract)
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
            ManagerController().create_new_contract(session=session)
            mock_confirm.assert_called_once_with(
                section="Create new Contract", session=session, msg="Operation Cancelled!"
            )

    def test_display_all_event(self, db_session, users, current_user_is_manager, mocker):
        # test should call a display_element.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_all_events", return_value=list_collab)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            ManagerController().display_all_event(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_event_without_events(self, db_session, users, current_user_is_manager, mocker):
        # test should call a no data message.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_all_events", return_value=list_collab)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().display_all_event(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_event_without_supporter(self, db_session, users, current_user_is_manager, mocker):
        # test should call a display_element.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_all_event_without_support", return_value=list_collab)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            ManagerController().display_all_event_without_supporter(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_event_without_supporter_without_events(
        self, db_session, users, current_user_is_manager, mocker
    ):
        # test should call a message no data.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_all_event_without_support", return_value=list_collab)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().display_all_event_without_supporter(session=session)
            mock_display_elements.assert_called_once()

    def test_display_customer_without_seller(self, db_session, users, current_user_is_manager, mocker):
        # test should call a display_customer_without_seller.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_customer_without_seller", return_value=list_collab)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            ManagerController().display_customer_without_seller(session=session)
            mock_display_elements.assert_called_once()

    def test_display_customer_without_seller_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should call a message no data.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_customer_without_seller", return_value=list_collab)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().display_customer_without_seller(session=session)
            mock_display_elements.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_display_event(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a good element to display according to user 's choice.
        with db_session as session:
            users
            current_user_is_manager
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 2]
            mock_display_all_event = mocker.patch.object(ManagerController, "display_all_event")
            mock_display_all_event_without_supporter = mocker.patch.object(
                ManagerController, "display_all_event_without_supporter"
            )
            ManagerController().display_event(session=session)
            if choice == 0:
                mock_display_all_event.assert_called_once()
            elif choice == 1:
                mock_display_all_event_without_supporter.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3), (4)])
    def test_update_element(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should a return a good function according to user's choice.
        with db_session as session:
            users
            current_user_is_manager
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 5]
            mock_collaborator = mocker.patch.object(ManagerController, "update_collaborator")
            mock_contract = mocker.patch.object(ManagerController, "update_contract")
            mock_update_customer_without_seller = mocker.patch.object(
                ManagerController, "update_customer_without_seller"
            )
            mock_update_event = mocker.patch.object(ManagerController, "update_event")
            mock_update_address = mocker.patch.object(Utils, "update_address")
            ManagerController().update_element(session=session)
            if choice == 0:
                mock_collaborator.assert_called_once()
            elif choice == 1:
                mock_contract.assert_called_once()
            elif choice == 2:
                mock_update_customer_without_seller.assert_called_once()
            elif choice == 3:
                mock_update_event.assert_called_once()
            elif choice == 4:
                mock_update_address.assert_called_once()

    @pytest.mark.parametrize("collaborator", [("Manager"), ("Seller"), ("Supporter")])
    def test__get_departement_list(self, db_session, users, current_user_is_manager, mocker, collaborator):
        # test should return available department list for change user's department.
        with db_session:
            user = users[0]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.models.utils.Utils.get_type_of_user", return_value=collaborator)
            if user == "Manager":
                assert manager._get_department_list(user) == ["Seller", "Supporter"]
            elif user == "Seller":
                assert manager._get_department_list(user) == ["Manager", "Supporter"]
            elif user == "Supporter":
                assert manager._get_department_list(user) == ["Manager", "Seller"]

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test__select_new_department(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a good element list according to user's choice.
        with db_session as session:
            user = users[0]
            current_user_is_manager
            manager = ManagerController()
            returned_list = ["A", "B"]
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._get_department_list",
                return_value=returned_list,
            )
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            if choice == 0:
                assert manager.select_new_department(section="", session=session, collaborator=user) == "A"
            elif choice == 1:
                assert manager.select_new_department(section="", session=session, collaborator=user) == "B"

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_collaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a wright user selected.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]

            mocker.patch("crm.models.users.Manager.get_all_users", return_value=list_collab)
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=list_collab[choice],
            )
            result = ManagerController().select_collaborator(session=session)
            assert result == list_collab[choice]

    def test_select_collaborator_without_collaborator(self, db_session, users, current_user_is_manager, mocker):
        # test should return a wright user selected.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []

            mocker.patch("crm.models.users.Manager.get_all_users", return_value=list_collab)
            result = ManagerController().select_collaborator(session=session)
            assert result is None

    def test_change_collaborator_department(self, db_session, users, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_new_department", return_value="Supporter"
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_update = mocker.patch.object(Manager, "change_user_department")
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")

            ManagerController().change_collaborator_department(session=session, collaborator_selected=users[1])
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation succesfull!"
            )
            mock_update.assert_called_once()

    def test_change_collaborator_department_with_no_confirm(self, db_session, users, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_new_department", return_value="Supporter"
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().change_collaborator_department(session=session, collaborator_selected=users[1])
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation Cancelled!"
            )

    @pytest.mark.parametrize(
        "choice, new_value",
        [
            ("name", "toto"),
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
            mock_update = mocker.patch.object(Manager, "update_user")
            ManagerController().change_collaborator_attribute(
                session=session, collaborator_selected=users[2], attribute_selected=choice
            )
            mock_update.assert_called_once()
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation succesfull!"
            )

    def test_change_collaborator_attribute_with_no_confirm(
        self,
        db_session,
        users,
        current_user_is_manager,
        mocker,
    ):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value="name")
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Manager, "update_user")
            ManagerController().change_collaborator_attribute(
                session=session, collaborator_selected=users[2], attribute_selected="name"
            )
            mock_update.assert_not_called()
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation Cancelled!"
            )

    def test_change_password(self, db_session, users, current_user_is_manager, mocker):
        # test should retrun call upadte user and confirm message.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mocker.patch("crm.view.user_view.UserView._get_user_password", return_value="password")
            ManagerController().change_password(session=session, collaborator_selected=users[2])
            assert users[2].password == "password"
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation succesfull!"
            )

    def test_change_password_with_no_confirm(self, db_session, users, current_user_is_manager, mocker):
        # test should retrun message and not called update user.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Manager, "update_user")
            mocker.patch("crm.view.user_view.UserView._get_user_password", return_value="password")
            ManagerController().change_password(session=session, collaborator_selected=users[2])
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation Cancelled!"
            )
            mock_update.assert_not_called()

    def test_change_email(self, db_session, users, current_user_is_manager, mocker):
        # test should return a user with new email address.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_update = mocker.patch.object(Manager, "update_user")
            mocker.patch("crm.view.user_view.UserView._get_email", return_value="email")
            ManagerController().change_email(session=session, collaborator_selected=users[2])
            mock_update.assert_called_once()
            mock_confirm.assert_called_once()

    def test_change_email_no_confirm(self, db_session, users, current_user_is_manager, mocker):
        # test should return an error message and not call update_user.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Manager, "update_user")
            mocker.patch("crm.view.user_view.UserView._get_email", return_value="")
            ManagerController().change_email(session=session, collaborator_selected=users[2])
            mock_confirm.assert_called_once_with(
                section=" Update Collaborator", session=session, msg="Operation Cancelled!"
            )
            mock_update.assert_not_called()

    @pytest.mark.parametrize(
        "choice",
        [("name"), ("email_address"), ("phone_number"), ("password"), ("department")],
    )
    def test_update_collaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a updated attribute of user selected.
        with db_session as session:
            user = users[1]
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_collaborator",
                return_value=user,
            )
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value=choice,
            )
            mock_department = mocker.patch.object(ManagerController, "change_collaborator_department")
            mock_password = mocker.patch.object(ManagerController, "change_password")
            mock_email = mocker.patch.object(ManagerController, "change_email")
            mock_attribute = mocker.patch.object(ManagerController, "change_collaborator_attribute")
            ManagerController().update_collaborator(session=session)
            if choice == "department":
                mock_department.assert_called_once()
            elif choice == "password":
                mock_password.assert_called_once()
            elif choice == "email_address":
                mock_email.assert_called_once()
            else:
                mock_attribute.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_contract(self, db_session, contracts, users, current_user_is_manager, mocker, choice):
        # test should retrun a good element selected by user.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]

            mocker.patch("crm.models.users.Manager.get_all_contracts", return_value=list_collab)
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )

            result = ManagerController().select_contract(session=session)
            assert result == list_collab[choice]

    def test_select_contract_without_contract(self, db_session, users, current_user_is_manager, mocker):
        # test should reti=urn None with empty list.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_all_contracts", return_value=list_collab)
            result = ManagerController().select_contract(session=session)
            assert result is None

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_change_customer_contract(
        self, db_session, contracts, clients, users, current_user_is_manager, mocker, choice
    ):
        # test should change customers of contracts.
        with db_session as session:
            users
            clients
            contracts
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_update = mocker.patch.object(Manager, "update_contract")
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            ManagerController().change_customer_of_contract(session=session, contract_selected=contracts[0])
            mock_update.assert_called_once()
            mock_confirm.assert_called_once_with(
                session=session, section=" Update Contract", msg="Operation succesfull!"
            )

    def test_change_customer_contract_no_confirm(
        self, db_session, contracts, clients, users, current_user_is_manager, mocker
    ):
        # test should return msg cancellation..
        with db_session as session:
            users
            clients
            contracts
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Manager, "update_contract")
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_customer_of_contract",
                return_value="choice",
            )
            ManagerController().change_customer_of_contract(session=session, contract_selected=contracts[0])
            mock_update.assert_not_called()
            mock_confirm.assert_called_once_with(
                section=" Update Contract", session=session, msg="Operation Cancelled!"
            )
            mock_update.assert_not_called()

    @pytest.mark.parametrize(
        " name,new_value",
        [
            ("total_amount", 15),
            ("remaining", 1),
            ("signed_contract", True),
        ],
    )
    def test_change_attribute_contract(
        self, db_session, contracts, users, current_user_is_manager, mocker, name, new_value
    ):
        # test should change attribute of contracts.
        with db_session as session:
            users
            contracts
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_update = mocker.patch.object(Manager, "update_contract")
            mocker.patch(
                "crm.view.generic_view.GenericView.get_new_value_of_attribute",
                return_value=new_value,
            )
            ManagerController().change_attribute_contract(
                session=session, attribute_selected=name, contract_selected=contracts[0]
            )
            mock_update.assert_called_once_with(contract=contracts[0], attribute_update=name, new_value=new_value)
            mock_confirm.assert_called_once_with(
                session=session, section=" Update Contract", msg="Operation succesfull!"
            )

    def test_change_attribute_contract_no_confirm(
        self, db_session, contracts, clients, users, current_user_is_manager, mocker
    ):
        # test should return msg cancellation..
        with db_session as session:
            users
            clients
            contracts
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Manager, "update_contract")
            mocker.patch(
                "crm.view.generic_view.GenericView.get_new_value_of_attribute",
                return_value="choice",
            )
            ManagerController().change_attribute_contract(
                session=session, attribute_selected="signed_contract", contract_selected=contracts[0]
            )
            mock_update.assert_not_called()
            mock_confirm.assert_called_once_with(
                section=" Update Contract", session=session, msg="Operation Cancelled!"
            )

    def test_update_contract_with_none(self, db_session, contracts, clients, users, current_user_is_manager, mocker):
        # test should return message error with empty contract list.
        with db_session as session:
            users
            clients
            contracts
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_contract",
                return_value=None,
            )
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().update_contract(session=session)
            mock_confirm.assert_called_once_with(
                session=session,
                section="Update Contract",
                msg="There are no availble contract. Update is not possible!",
            )

    def test_update_contract_with_attribute_is_customer(
        self, db_session, contracts, clients, users, current_user_is_manager, mocker
    ):
        # test should call wright function with customer like attribute to updated.
        with db_session as session:
            users
            clients
            contract = contracts[0]
            current_user_is_manager
            mocker.patch("crm.controller.manager_controller.ManagerController.select_contract", return_value=contract)
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value="customer")
            mock_change_customer_of_contract = mocker.patch.object(ManagerController, "change_customer_of_contract")
            ManagerController().update_contract(session=session)
            mock_change_customer_of_contract.assert_called_once()

    def test_update_contract_other_attribute_customer(
        self, db_session, contracts, clients, users, current_user_is_manager, mocker
    ):
        # test should return message error with empty contract list.
        with db_session as session:
            users
            clients
            contract = contracts[0]
            current_user_is_manager
            mocker.patch("crm.controller.manager_controller.ManagerController.select_contract", return_value=contract)
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value="total_amount")
            mock_change = mocker.patch.object(ManagerController, "change_attribute_contract")
            ManagerController().update_contract(session=session)
            mock_change.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_customer_without_seller(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return wright supporter.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_customer_without_seller", return_value=list_collab)
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            result = ManagerController().select_customer_without_seller(session=session)
            assert result == list_collab[choice]

    def test_select_customer_without_seller_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should reti=urn None with empty list.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_customer_without_seller", return_value=list_collab)
            result = ManagerController().select_customer_without_seller(session=session)
            assert result is None

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_seller(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return wright supporter.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.controller.manager_controller.ManagerController.get_seller", return_value=list_collab)
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            result = ManagerController().select_seller(session=session)
            assert result == list_collab[choice]

    def test_select_seller_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should reti=urn None with empty list.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.controller.manager_controller.ManagerController.get_seller", return_value=list_collab)
            result = ManagerController().select_seller(session=session)
            assert result is None

    def test_update_customer_without_seller(self, db_session, users, clients, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            client = clients[0]
            seller2 = Seller(name="seller_2", email_address="hhh@", password="password")
            session.add(seller2)
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_customer_without_seller",
                return_value=client,
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mocker.patch("crm.controller.manager_controller.ManagerController.select_seller", return_value=seller2)
            ManagerController().update_customer_without_seller(session=session)
            assert client.seller_contact == seller2
            mock_confirm.assert_called_once()

        def test_update_customer_without_seller_no_confirm(
            self, db_session, users, clients, current_user_is_manager, mocker
        ):
            with db_session as session:
                users
                current_user_is_manager
                clients[0]
                seller2 = Seller(name="seller_2", email_address="hhh@", password="password")
                session.add(seller2)
                mocker.patch(
                    "crm.controller.manager_controller.ManagerController.select_customer_without_seller",
                    return_value=seller2,
                )
                mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
                mock_confirm = mocker.patch.object(GenericView, "no_data_message")
                mocker.patch("crm.controller.manager_controller.ManagerController.select_seller", return_value=seller2)
                ManagerController().update_customer_without_seller(session=session)
                mock_confirm.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_supporter(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return wright supporter.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_all_supporter", return_value=list_collab)
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            result = ManagerController().select_supporter(session=session)
            assert result == list_collab[choice]

    def test_select_supporter_without_contract(self, db_session, users, current_user_is_manager, mocker):
        # test should reti=urn None with empty list.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_all_supporter", return_value=list_collab)
            result = ManagerController().select_supporter(session=session)
            assert result is None

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_event(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return wright supporter.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = ["A", "B", "C"]
            mocker.patch("crm.models.users.Manager.get_all_events", return_value=list_collab)
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            result = ManagerController().select_event(session=session)
            assert result == list_collab[choice]

    def test_select_event_without_contract(self, db_session, users, current_user_is_manager, mocker):
        # test should reti=urn None with empty list.
        with db_session as session:
            users
            current_user_is_manager
            list_collab = []
            mocker.patch("crm.models.users.Manager.get_all_events", return_value=list_collab)
            result = ManagerController().select_event(session=session)
            assert result is None

    def test_update_event_with_no_event(self, db_session, users, current_user_is_manager, mocker):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.controller.manager_controller.ManagerController.select_event", return_value=None)
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_supporter", return_value="supporter_2"
            )
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().update_event(session=session)
            mock_confirm.assert_called_once_with(
                session=session,
                section=" Update event",
                msg="There are no available Event or Supporter. Update Event is not possible!",
            )

    def test_update_event_with_no_supporter(self, db_session, users, current_user_is_manager, mocker):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.controller.manager_controller.ManagerController.select_event", return_value="event")
            mocker.patch("crm.controller.manager_controller.ManagerController.select_supporter", return_value=None)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().update_event(session=session)
            mock_confirm.assert_called_once_with(
                session=session,
                section=" Update event",
                msg="There are no available Event or Supporter. Update Event is not possible!",
            )

    def test_update_event_with_confirm(self, db_session, users, events, current_user_is_manager, mocker):
        # test should return a call of update function of event.
        with db_session as session:
            user = users[2]
            current_user_is_manager
            event = events[1]
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.controller.manager_controller.ManagerController.select_event", return_value=event)
            mocker.patch("crm.controller.manager_controller.ManagerController.select_supporter", return_value=user)
            mock_update = mocker.patch.object(Manager, "change_supporter_of_event")
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")

            ManagerController().update_event(session=session)
            mock_update.assert_called_once()
            mock_confirm.assert_called_once_with(session=session, section=" Update event", msg="Operation succesfull!")

    def test_update_event_with_no_confirm(self, db_session, users, events, current_user_is_manager, mocker):
        # test should return a call of update function of event.
        with db_session as session:
            user = users[2]
            current_user_is_manager
            event = events[1]
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.controller.manager_controller.ManagerController.select_event", return_value=event)
            mocker.patch("crm.controller.manager_controller.ManagerController.select_supporter", return_value=user)
            mock_update = mocker.patch.object(Manager, "change_supporter_of_event")
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")

            ManagerController().update_event(session=session)
            mock_update.assert_not_called()
            mock_confirm.assert_called_once_with(session=session, section=" Update event", msg="Operation Cancelled!")

    def test_select_and_delete_collaborator(self, db_session, users, current_user_is_manager, mocker):
        # test should call delete function after confirm.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value="user",
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_delete = mocker.patch.object(Manager, "delete_collaborator")
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            ManagerController().select_and_delete_collaborator(
                session=session, section=" Delete collaborator", collaborator_list=users
            )
            mock_delete.assert_called_once()
            mock_confirm.assert_called_once_with(
                session=session, section=" Delete collaborator", msg="Operation succesfull!"
            )

    def test_select_and_delete_collaborator_with_no_confirm(self, db_session, users, current_user_is_manager, mocker):
        # test should call delete function after confirm.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value="user",
            )
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_delete = mocker.patch.object(Manager, "delete_collaborator")
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().select_and_delete_collaborator(
                session=session, section=" Delete collaborator", collaborator_list=users
            )
            mock_delete.assert_not_called()
            mock_confirm.assert_called_once_with(
                session=session, section=" Delete collaborator", msg="Operation Cancelled!"
            )

    def test_delete_collaborator(self, db_session, users, current_user_is_manager, mocker):
        # Test should retrun a user less one.
        with db_session as session:
            users
            user = current_user_is_manager
            mocker.patch("crm.models.users.Manager.get_all_users", return_value=[user, users[0], users[1], users[2]])
            mock_delete = mocker.patch.object(ManagerController, "select_and_delete_collaborator")
            ManagerController().delete_collaborator(session=session)
            mock_delete.assert_called_once()

    def test_delete_collaborator_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # Test should retrun a user less one.
        with db_session as session:
            users
            user = current_user_is_manager
            mocker.patch("crm.models.users.Manager.get_all_users", return_value=[user])
            mock_delete = mocker.patch.object(ManagerController, "select_and_delete_collaborator")
            mock_msg = mocker.patch.object(GenericView, "no_data_message")
            ManagerController().delete_collaborator(session=session)
            mock_delete.assert_not_called()
            mock_msg.assert_called_once_with(
                session=session,
                section="Delete collaborator",
                msg="There are no available collaborator. Delete is not possible!",
            )
