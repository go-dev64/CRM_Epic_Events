import pytest
from sqlalchemy import select
from crm.controller.manager_controller import ManagerController
from crm.models.element_administratif import Contract
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
            result = ManagerController().create_new_contract(session=session)
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

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_update_element(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should a return a good function according to user's choice.
        with db_session as session:
            users
            current_user_is_manager
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 4]
            mock_collaborator = mocker.patch.object(ManagerController, "update_collaborator")
            mock_contract = mocker.patch.object(ManagerController, "update_contract")
            mock_update_event = mocker.patch.object(ManagerController, "update_event")
            mock_update_address = mocker.patch.object(Utils, "update_address")
            ManagerController().update_element(session=session)
            if choice == 0:
                mock_collaborator.assert_called_once()
            elif choice == 1:
                mock_contract.assert_called_once()
            elif choice == 2:
                mock_update_event.assert_called_once()
            elif choice == 3:
                mock_update_address.assert_called_once()

    @pytest.mark.parametrize("collaborator", [("Manager"), ("Seller"), ("Supporter")])
    def test__get_departement_list(self, db_session, users, current_user_is_manager, mocker, collaborator):
        # test should return available department list for change user's department.
        with db_session as session:
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
            assert result == None

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
            ManagerController().change_collaborator_attribute(
                session=session, collaborator_selected=users[2], attribute_selected=choice
            )
            assert getattr(users[2], choice) == new_value
        
        
    def test_change_collaborator_attribute(
        self, db_session, users, current_user_is_manager, mocker, choice, new_value
    ):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            ManagerController().change_collaborator_attribute(
                session=session, collaborator_selected=users[2], attribute_selected=choice
            )
            assert getattr(users[2], choice) == new_value

    def test_change_password(self, db_session, users, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.user_view.UserView._get_user_password", return_value="password")
            ManagerController().change_password(session=session, collaborator_selected=users[2])
            assert users[2].password == "password"

    @pytest.mark.parametrize(
        "choice",
        [("name"), ("email_address"), ("phone_number"), ("password"), ("department")],
    )
    def test_update_collaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a updated attribute of user selected.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_collaborator",
                return_value=users[1],
            )
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value=choice,
            )
            mock_department = mocker.patch.object(ManagerController, "change_collaborator_department", return_value="")
            mock_password = mocker.patch.object(ManagerController, "change_password", return_value="")
            mock_attribute = mocker.patch.object(ManagerController, "change_collaborator_attribute", return_value="")
            ManagerController().update_collaborator(session=session)
            if choice == "department":
                mock_department.assert_called_once()
            elif choice == "password":
                mock_password.assert_called_once()
            else:
                mock_attribute.assert_called_once()

    """def test_change_user_departement(self, db_session, users, current_user_is_manager, mocker):
        # Test should change user of department. the number of User is the same.
        with db_session as session:
            user = users[1]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_collaborator",
                return_value=user,
            )
            mocker.patch(
                "crm.models.utils.Utils._select_attribut_of_element",
                return_value="department",
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_new_department",
                return_value="Supporter",
            )
            manager.update_collaborator(session=session)
            list_user = session.scalars(select(User)).all()
            list_supporter = session.scalars(select(Supporter)).all()
            assert new_user.department == "supporter_table"
            assert len(list_user) == 3
            assert len(list_supporter) == 2"""

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
            assert result == None

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
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            ManagerController().change_customer_of_contract(session=session, contract_selected=contracts[0])
            assert contracts[0].customer == clients[choice]

    @pytest.mark.parametrize(
        "choice, name,new_value",
        [
            (1, "total_amount", 15),
            (2, "remaining", 1),
            (3, "signed_contract", True),
        ],
    )
    def test_update_contract(
        self, db_session, contracts, clients, users, current_user_is_manager, mocker, choice, new_value, name
    ):
        with db_session as session:
            users
            clients
            contracts
            current_user_is_manager
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=contracts[0],
            )
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value=new_value)
            mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value=new_value)
            mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value=new_value)
            ManagerController().update_contract(session=session)
            assert getattr(contracts[0], name) == new_value

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
            assert result == None

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
            assert result == None

    def test_update_event(self, db_session, events, users, current_user_is_manager, mocker):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            events
            current_user_is_manager
            supporter_2 = Supporter(
                name="supporter_2", email_address="email_supporter2", phone_number="023153", password="35516"
            )
            session.add(supporter_2)
            manager = ManagerController()
            mocker.patch("crm.controller.manager_controller.ManagerController.select_event", return_value=events[0])
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_supporter", return_value=supporter_2
            )
            manager.update_event(session=session)
            assert events[0].supporter == supporter_2

    def test_delete_collaborator(self, db_session, users, current_user_is_manager, mocker):
        # Test should retrun a user less one.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.models.users.Manager.get_all_users", return_value=[x for x in users])
            mocker.patch(
                "crm.models.utils.Utils._select_element_in_list",
                return_value=users[1],
            )

            manager.delete_collaborator(session=session)
            user_list = session.scalars(select(User)).all()
            seller_list = session.scalars(select(Seller)).all()
            assert len(user_list) == 2
            assert len(seller_list) == 0
