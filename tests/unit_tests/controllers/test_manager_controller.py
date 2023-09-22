import pytest
from sqlalchemy import select
from crm.controller.manager_controller import ManagerController
from crm.models.users import Supporter, User


class TestManagerController:
    @pytest.mark.parametrize("choice", [(1), (2)])
    def test_create_new_element(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a good function to according user's choice.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.create_new_user",
                return_value="create_new_user",
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.create_new_contract",
                return_value="create_new_contract",
            )
            if choice == 1:
                assert manager.create_new_element(session=session) == "create_new_user"
            elif choice == 2:
                assert manager.create_new_element(session=session) == "create_new_contract"
            else:
                pass

    @pytest.mark.parametrize("department", [(1), (2), (3)])
    def test_create_new_user(self, db_session, users, current_user_is_manager, mocker, department):
        # test should return a good function of creating user according to user's choice..
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=department)
            mocker.patch("crm.models.users.Manager.create_new_manager", return_value="new_manager")
            mocker.patch("crm.models.users.Manager.create_new_seller", return_value="new_seller")
            mocker.patch("crm.models.users.Manager.create_new_supporter", return_value="new_supporter")

            if department == 1:
                assert manager.create_new_user(session=session) == "new_manager"
            elif department == 2:
                assert manager.create_new_user(session=session) == "new_seller"
            elif department == 3:
                assert manager.create_new_user(session=session) == "new_supporter"

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_display_event(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return a good element to display according to user 's choice.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_event_to_display",
                return_value="Display all Events",
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.select_event_without_supporter_to_display",
                return_value="Display all Events without Supporter",
            )
            if choice == 0:
                assert manager.display_event(session=session) == "Display all Events"
            elif choice == 1:
                assert manager.display_event(session=session) == "Display all Events without Supporter"

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_update_element(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should a return a good function according to user's choice.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.update_collaborator",
                return_value="update_collaborator",
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.update_contract", return_value="update_contract"
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.update_event", return_value="update_event"
            )
            mocker.patch("crm.models.utils.Utils.update_address", return_value="update_address")

            if choice == 0:
                assert manager.update_element(session=session) == "update_collaborator"
            elif choice == 1:
                assert manager.update_element(session=session) == "update_contract"
            elif choice == 2:
                assert manager.update_element(session=session) == "update_event"
            elif choice == 3:
                assert manager.update_element(session=session) == "update_address"

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test__select_colaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should return the good element of list according to usre's choice.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()
            returned_list = ["A", "B", "C"]
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch("crm.models.users.Manager.get_all_users", return_value=returned_list)
            if choice == 0:
                assert manager._select_collaborator(session=session) == "A"
            elif choice == 1:
                assert manager._select_collaborator(session=session) == "B"
            elif choice == 2:
                assert manager._select_collaborator(session=session) == "C"

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3), (4)])
    def test__select_attribute_collaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # test should retrun a good user attribure according a user's choice.
        with db_session as session:
            users
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            if choice == 0:
                assert manager._select_attribute_collaborator() == "name"
            elif choice == 1:
                assert manager._select_attribute_collaborator() == "email_address"
            elif choice == 2:
                assert manager._select_attribute_collaborator() == "phone_number"
            elif choice == 3:
                assert manager._select_attribute_collaborator() == "password"
            elif choice == 4:
                assert manager._select_attribute_collaborator() == "department"

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
    def test__select_new_department(self, db_session, users, mocker, choice):
        # test should return a good element list according to user's choice.
        with db_session as session:
            user = users[0]
            manager = ManagerController()
            returned_list = ["A", "B"]
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._get_department_list",
                return_value=returned_list,
            )
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            if choice == 0:
                assert manager._select_new_department(user) == "A"
            elif choice == 1:
                assert manager._select_new_department(user) == "B"

    @pytest.mark.parametrize(
        "choice, new_value",
        [
            ("name", "toto"),
            ("email_address", "email@dfkjnekr"),
            ("phone_number", "12351"),
            ("password", "passwrgeord"),
        ],
    )
    def test_update_collaborator(self, db_session, users, current_user_is_manager, mocker, choice, new_value):
        # test should return a updated attribute of user selected.
        with db_session as session:
            user = users[1]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._select_collaborator",
                return_value=user,
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._get_new_collaborator_attribute",
                return_value=new_value,
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._select_attribute_collaborator",
                return_value=choice,
            )

            if choice == "name":
                manager.update_collaborator(session=session)
                assert user.name == new_value
            elif choice == "email_addres":
                manager.update_collaborator(session=session)
                assert user.email_address == new_value
            elif choice == "phone_number":
                manager.update_collaborator(session=session)
                assert user.phone_number == new_value
            elif choice == "paassword":
                manager.update_collaborator(session=session)
                assert user.password == new_value

    def test_change_user_departement(self, db_session, users, current_user_is_manager, mocker):
        # Test should change user of department. the number of User is the same.
        with db_session as session:
            user = users[1]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._select_collaborator",
                return_value=user,
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._select_attribute_collaborator",
                return_value="department",
            )
            mocker.patch(
                "crm.controller.manager_controller.ManagerController._select_new_department",
                return_value="supporter",
            )
            new_user = manager.update_collaborator(session=session)
            list_user = session.scalars(select(User)).all()
            list_supporter = session.scalars(select(Supporter)).all()
            assert new_user.department == "supporter_table"
            assert len(list_user) == 3
            assert len(list_supporter) == 2
