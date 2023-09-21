import pytest
from crm.controller.manager_controller import ManagerController


class TestManagerController:
    @pytest.mark.parametrize("choice", [(1), (2)])
    def test_create_new_element(self, db_session, users, current_user_is_manager, mocker, choice):
        with db_session as session:
            users
            current_user_is_manager
            manager_ctrl = ManagerController()

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
                assert manager_ctrl.create_new_element(session=session) == "create_new_user"
            elif choice == 2:
                assert manager_ctrl.create_new_element(session=session) == "create_new_contract"
            else:
                pass

    @pytest.mark.parametrize("department", [(1), (2), (3)])
    def test_create_new_user(self, db_session, users, current_user_is_manager, mocker, department):
        with db_session as session:
            users
            current_user_is_manager
            manager_ctrl = ManagerController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=department)
            mocker.patch("crm.models.users.Manager.create_new_manager", return_value="new_manager")
            mocker.patch("crm.models.users.Manager.create_new_seller", return_value="new_seller")
            mocker.patch("crm.models.users.Manager.create_new_supporter", return_value="new_supporter")

            if department == 1:
                assert manager_ctrl.create_new_user(session=session) == "new_manager"
            elif department == 2:
                assert manager_ctrl.create_new_user(session=session) == "new_seller"
            elif department == 3:
                assert manager_ctrl.create_new_user(session=session) == "new_supporter"

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_update_element(self, db_session, users, current_user_is_manager, mocker, choice):
        with db_session as session:
            users
            current_user_is_manager
            manager_ctrl = ManagerController()

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
                assert manager_ctrl.update_element(session=session) == "update_collaborator"
            elif choice == 1:
                assert manager_ctrl.update_element(session=session) == "update_contract"
            elif choice == 2:
                assert manager_ctrl.update_element(session=session) == "update_event"
            elif choice == 3:
                assert manager_ctrl.update_element(session=session) == "update_address"

    def test_update_collaborator(self, db_session, users, current_user_is_manager, mocker, choice):
        # commet
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
