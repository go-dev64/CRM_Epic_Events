import pytest

from crm.controller.user_controller import UserController


class TestIntegrationUserController:
    def test_user_choice_is_deleting_with_manager(self, db_session, users, current_user_is_manager, mocker):
        with db_session as session:
            users
            current_user_is_manager
            controller = UserController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.delete_collaborator",
                return_value="delete_collaborator",
            )
            assert controller.user_choice_is_deleting(session=session) == "delete_collaborator"

    def test_user_choice_is_deleting_with_seller(self, db_session, users, current_user_is_seller, mocker):
        with db_session as session:
            users
            current_user_is_seller
            controller = UserController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.delete_collaborator",
                return_value="delete_collaborator",
            )
            assert controller.user_choice_is_deleting(session=session) == None

    def test_user_choice_is_deleting_with_supporter(self, db_session, users, current_user_is_supporter, mocker):
        with db_session as session:
            users
            current_user_is_supporter
            controller = UserController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.delete_collaborator",
                return_value="delete_collaborator",
            )
            assert controller.user_choice_is_deleting(session=session) == None
