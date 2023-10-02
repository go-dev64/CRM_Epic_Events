import pytest
from crm.controller.manager_controller import ManagerController
from crm.controller.seller_controller import SellerController
from crm.controller.supporter_controller import SupporterController
from crm.controller.user_controller import UserController
from crm.models.users import User
from crm.models.utils import Utils
from crm.view.generic_view import GenericView


class TestUserController:
    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_home_page(self, db_session, users, current_user_is_user, mocker, choice):
        # test check if the wright function is returned according to user's choise.
        with db_session as session:
            users
            current_user_is_user
            user_ctr = UserController()

            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 4]
            mock_create = mocker.patch.object(UserController, "user_choice_is_creating")
            mock_read = mocker.patch.object(UserController, "user_choice_is_reading")
            mock_update = mocker.patch.object(UserController, "user_choice_is_updating")
            mock_delete = mocker.patch.object(UserController, "user_choice_is_deleting")
            user_ctr.home_page(session=session)
            if choice == 0:
                mock_create.assert_called_once()
            elif choice == 1:
                mock_read.assert_called_once()
            elif choice == 2:
                mock_update.assert_called_once()
            elif choice == 3:
                mock_delete.assert_called_once()

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_user_choice_is_creating(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            mock_manager = mocker.patch.object(ManagerController, "create_new_element")
            mock_seller = mocker.patch.object(SellerController, "create_new_element")
            mock_suporter = mocker.patch.object(Utils, "create_new_address")
            UserController().user_choice_is_creating(session=session)
            if user == "Manager":
                mock_manager.assert_called_once()
            elif user == "Seller":
                mock_seller.assert_called_once()
            elif user == "Supporter":
                mock_suporter.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    # test check if the wright function is returned according to user's choice.
    def test_user_choice_is_reading(self, db_session, users, current_user_is_user, mocker, choice):
        with db_session as session:
            users
            current_user_is_user

            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 4]
            mock_customer = mocker.patch.object(UserController, "get_customer_list")
            mock_contract = mocker.patch.object(UserController, "get_contract_list")
            mock_event = mocker.patch.object(UserController, "get_events_list")
            mock_address = mocker.patch.object(UserController, "get_address_list")
            UserController().user_choice_is_reading(session=session)

            if choice == 0:
                mock_customer.assert_called_once()
            elif choice == 1:
                mock_contract.assert_called_once()
            elif choice == 2:
                mock_event.assert_called_once()
            elif choice == 3:
                mock_address.assert_called_once()

    def test_get_customer_list_with_seller_user(self, db_session, users, current_user_is_seller, mocker):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_seller
            mock_seller = mocker.patch.object(SellerController, "select_customer_type_to_display")
            UserController().get_customer_list(session=session)
            mock_seller.assert_called_once()

    def test_get_customer_list_with_other_user_of_seler(self, db_session, users, current_user_is_manager, mocker):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.models.users.User.get_all_customers", return_value=[1, 2, 3, 4])
            mock_utils = mocker.patch.object(GenericView, "display_elements", return_value="")
            UserController().get_customer_list(session=session)
            mock_utils.assert_called_once()

    def test_get_customer_list_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should retrun a no data msh if len customer list ==0.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.models.users.User.get_all_customers", return_value=[])
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_customer_list(session=session)
            mock_generic.assert_called_once()

    def test_get_contract_list_with_other_user_of_seler(self, db_session, users, current_user_is_manager, mocker):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.models.users.User.get_all_contracts", return_value=[1, 2, 3, 4])
            mock_utils = mocker.patch.object(GenericView, "display_elements", return_value="")
            UserController().get_contract_list(session=session)
            mock_utils.assert_called_once()

    def test_get_contract_list_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should retrun a no data msh if len customer list ==0.
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.models.users.User.get_all_contracts", return_value=[])
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_contract_list(session=session)
            mock_generic.assert_called_once()

    def test_get_contract_list_with_seller_user(self, mocker, db_session, users, current_user_is_seller):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_seller
            mock_seller = mocker.patch.object(SellerController, "select_contract_type_to_display", return_value="")
            UserController().get_contract_list(session=session)
            mock_seller.assert_called_once()

    def test_get_event_list_with_supporter(self, db_session, users, current_user_is_supporter, mocker):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_supporter
            mock_supporter = mocker.patch.object(SupporterController, "display_event")
            UserController().get_events_list(session=session)
            mock_supporter.assert_called_once()

    def test_get_event_list_with_manager(self, db_session, users, current_user_is_manager, mocker):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_manager
            mock_supporter = mocker.patch.object(ManagerController, "display_event")
            UserController().get_events_list(session=session)
            mock_supporter.assert_called_once()

    def test_get_event_list_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should retrun a no data msg if len event list ==0.
        with db_session as session:
            users
            current_user_is_seller
            mocker.patch("crm.models.users.User.get_all_events", return_value=[])
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_events_list(session=session)
            mock_generic.assert_called_once()

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_get_address_list(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            mocker.patch("crm.models.users.User.get_all_adress", return_value=[1, 2, 3, 4])
            mock_utils = mocker.patch.object(GenericView, "display_elements", return_value="")
            UserController().get_address_list(session=session)
            mock_utils.assert_called_once()

    def test_get_address_list_with_no_data(self, db_session, users, current_user_is_user, mocker):
        # test should retrun a no data msg if len event list ==0.
        with db_session as session:
            users
            current_user_is_user
            mocker.patch("crm.models.users.User.get_all_adress", return_value=[])
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_address_list(session=session)
            mock_generic.assert_called_once()

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_user_choice_is_updating(self, db_session, users, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user

            mock_manager = mocker.patch.object(ManagerController, "update_element")
            mock_seller = mocker.patch.object(SellerController, "select_element_type_to_be_updated")
            mock_suporter = mocker.patch.object(SupporterController, "update_element")
            UserController().user_choice_is_updating(session=session)
            if user == "Manager":
                mock_manager.assert_called_once()
            elif user == "Seller":
                mock_seller.assert_called_once()
            elif user == "Supporter":
                mock_suporter.assert_called_once()

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_user_choice_is_deleting(self, db_session, users, current_user_is_user, mocker, user):
        with db_session as session:
            users
            current_user_is_user
            session.current_user_department = user
            mock_manager = mocker.patch.object(ManagerController, "delete_collaborator")
            mock_generic = mocker.patch.object(GenericView, "forbidden_acces")

            UserController().user_choice_is_deleting(session=session)
            if user == "Manager":
                mock_manager.assert_called_once()
            elif user == "Seller":
                mock_generic.assert_called_once()
            elif user == "Supporter":
                mock_generic.assert_called_once()
