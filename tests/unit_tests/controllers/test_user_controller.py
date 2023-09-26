import pytest
from crm.controller.user_controller import UserController


class TestUserController:
    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_home_page(self, db_session, users, current_user_is_user, mocker, choice):
        # test check if the wright function is returned according to user's choise.
        with db_session as session:
            users
            current_user_is_user
            user_ctr = UserController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.user_controller.UserController.user_choice_is_creating",
                return_value="user_choice_is_creating",
            )
            mocker.patch(
                "crm.controller.user_controller.UserController.user_choice_is_reading",
                return_value="user_choice_is_reading",
            )
            mocker.patch(
                "crm.controller.user_controller.UserController.user_choice_is_updating",
                return_value="user_choice_is_updating",
            )
            mocker.patch(
                "crm.controller.user_controller.UserController.user_choice_is_deleting",
                return_value="user_choice_is_deleting",
            )

            if choice == 0:
                assert user_ctr.home_page(session=session) == "user_choice_is_creating"
            elif choice == 1:
                assert user_ctr.home_page(session=session) == "user_choice_is_reading"
            elif choice == 2:
                assert user_ctr.home_page(session=session) == "user_choice_is_updating"
            elif choice == 3:
                assert user_ctr.home_page(session=session) == "user_choice_is_deleting"

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_user_choice_is_creating(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            user_ctr = UserController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.create_new_element",
                return_value="create_new_element_Manager",
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.create_new_element",
                return_value="create_new_element_Seller",
            )
            mocker.patch(
                "crm.models.utils.Utils.create_new_address",
                return_value="create_new_address",
            )

            if user == "Manager":
                assert user_ctr.user_choice_is_creating(session=session) == "create_new_element_Manager"
            elif user == "Seller":
                assert user_ctr.user_choice_is_creating(session=session) == "create_new_element_Seller"
            elif user == "Supporter":
                assert user_ctr.user_choice_is_creating(session=session) == "create_new_address"

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    # test check if the wright function is returned according to user's choice.
    def test_user_choice_is_reading(self, db_session, users, current_user_is_user, mocker, choice):
        with db_session as session:
            users
            current_user_is_user
            user_ctr = UserController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.user_controller.UserController.get_customer_list",
                return_value="get_customer_list",
            )
            mocker.patch(
                "crm.controller.user_controller.UserController.get_contract_list",
                return_value="get_contract_list",
            )
            mocker.patch(
                "crm.controller.user_controller.UserController.get_events_list",
                return_value="get_events_list",
            )
            if choice == 0:
                assert user_ctr.user_choice_is_reading(session=session) == "get_customer_list"
            elif choice == 1:
                assert user_ctr.user_choice_is_reading(session=session) == "get_contract_list"
            elif choice == 2:
                assert user_ctr.user_choice_is_reading(session=session) == "get_events_list"

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_get_customer_list(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            user_ctr = UserController()
            mocker.patch("crm.view.generic_view.GenericView.display_element", return_value=user)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.select_customer_type_to_display",
                return_value="Seller",
            )
            if user == "Manager":
                assert user_ctr.get_customer_list(session=session) == "Manager"
            elif user == "Seller":
                assert user_ctr.get_customer_list(session=session) == "Seller"
            elif user == "Supporter":
                assert user_ctr.get_customer_list(session=session) == "Supporter"

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_get_contract_list(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            user_ctr = UserController()

            mocker.patch("crm.view.generic_view.GenericView.display_element", return_value=user)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.select_contract_type_to_display",
                return_value="Seller",
            )
            if user == "Manager":
                assert user_ctr.get_contract_list(session=session) == "Manager"
            elif user == "Seller":
                assert user_ctr.get_contract_list(session=session) == "Seller"
            elif user == "Supporter":
                assert user_ctr.get_contract_list(session=session) == "Supporter"

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_get_event_list(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            user_ctr = UserController()
            mocker.patch("crm.view.generic_view.GenericView.display_element", return_value=user)
            mocker.patch("crm.controller.manager_controller.ManagerController.display_event", return_value=user)
            mocker.patch(
                "crm.controller.supporter_controller.SupporterController.display_event_of_user",
                return_value="Supporter!",
            )
            if user == "Manager":
                assert user_ctr.get_events_list(session=session) == "Manager"
            elif user == "Seller":
                assert user_ctr.get_events_list(session=session) == "Seller"
            elif user == "Supporter":
                assert user_ctr.get_events_list(session=session) == "Supporter!"

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_user_choice_is_updating(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            user_ctr = UserController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.update_element",
                return_value="update_element_Manager",
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.select_element_type_to_be_updated",
                return_value="update_element_Seller",
            )
            mocker.patch(
                "crm.controller.supporter_controller.SupporterController.update_element",
                return_value="update_element_supporter",
            )

            if user == "Manager":
                assert user_ctr.user_choice_is_updating(session=session) == "update_element_Manager"
            elif user == "Seller":
                assert user_ctr.user_choice_is_updating(session=session) == "update_element_Seller"
            elif user == "Supporter":
                assert user_ctr.user_choice_is_updating(session=session) == "update_element_supporter"

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_user_choice_is_deleting(self, db_session, users, current_user_is_manager, mocker, user):
        with db_session as session:
            users
            current_user_is_manager
            session.current_user_department = user
            controller = UserController()
            mocker.patch(
                "crm.controller.manager_controller.ManagerController.delete_collaborator",
                return_value="delete_collaborator",
            )
            if user == "Manager":
                assert controller.user_choice_is_deleting(session=session) == "delete_collaborator"
            elif user == "Seller":
                assert controller.user_choice_is_deleting(session=session) == None
            elif user == "Supporter":
                assert controller.user_choice_is_deleting(session=session) == None
