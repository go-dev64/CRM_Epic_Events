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
