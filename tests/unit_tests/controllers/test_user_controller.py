import pytest
from crm.controller.user_controller import UserController
from crm.controller.manager_controller import ManagerController
import crm.controller.user_controller
from crm.view.user_view import UserView


class TestUserController:
    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_home_page(self, db_session, users, current_user_is_user, mocker, choice):
        with db_session as session:
            users
            current_user_is_user
            user_ctr = UserController()

            mocker.patch("crm.view.user_view.UserView.view_select_choice", return_value=choice)

            if choice == 0:
                assert user_ctr.home_page(session=None) == user_ctr.user_choice_is_creating(session=None)
            elif choice == 1:
                assert user_ctr.home_page(session=None) == user_ctr.user_choice_is_reading(session=None)
            elif choice == 2:
                assert user_ctr.home_page(session=None) == user_ctr.user_choice_is_updating(session=None)
            elif choice == 3:
                assert user_ctr.home_page(session=None) == user_ctr.user_choice_is_deleting(session=None)

    def test_user_choice_is_creating(self, db_session, users, current_user_is_manager):
        with db_session as session:
            users
            current_user_is_manager
            user_ctr = UserController()
            assert user_ctr.user_choice_is_creating(session=None) == ManagerController().create_new_user(session=None)
