import pytest
from crm.controller.seller_controller import SellerController

from crm.controller.user_controller import UserController
from crm.view.generic_view import GenericView


class TestIntegrationUserController:
    def test_get_customer_list_with_other_user_of_seler(
        self, db_session, users, clients, current_user_is_manager, mocker
    ):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            clients
            current_user_is_manager
            mock_utils = mocker.patch.object(GenericView, "display_elements", return_value="")
            UserController().get_customer_list(session=session)
            mock_utils.assert_called_once()

    def test_get_customer_list_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should retrun a no data msh if len customer list ==0.
        with db_session as session:
            users
            current_user_is_manager
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_customer_list(session=session)
            mock_generic.assert_called_once()

    def test_get_contract_list_with_other_user_of_seler(
        self, db_session, contracts, users, current_user_is_manager, mocker
    ):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            contracts
            current_user_is_manager
            mock_utils = mocker.patch.object(GenericView, "display_elements", return_value="")
            UserController().get_contract_list(session=session)
            mock_utils.assert_called_once()

    def test_get_contract_list_with_no_data(self, db_session, users, current_user_is_manager, mocker):
        # test should retrun a no data msh if len customer list ==0.
        with db_session as session:
            users
            current_user_is_manager
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_contract_list(session=session)
            mock_generic.assert_called_once()

    def test_get_event_list_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should retrun a no data msg if len event list ==0.
        with db_session as session:
            users
            current_user_is_seller
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_events_list(session=session)
            mock_generic.assert_called_once()

    @pytest.mark.parametrize("user", [("Manager"), ("Seller"), ("Supporter")])
    def test_get_address_list(self, db_session, users, address, current_user_is_user, mocker, user):
        # test check if the wright function is returned according to current user's department.
        with db_session as session:
            users
            address
            current_user_is_user
            session.current_user_department = user
            mock_utils = mocker.patch.object(GenericView, "display_elements", return_value="")
            UserController().get_address_list(session=session)
            mock_utils.assert_called_once()

    def test_get_address_list_with_no_data(self, db_session, users, current_user_is_user, mocker):
        # test should retrun a no data msg if len event list ==0.
        with db_session as session:
            users
            current_user_is_user
            mock_generic = mocker.patch.object(GenericView, "no_data_message", return_value="no data")
            UserController().get_address_list(session=session)
            mock_generic.assert_called_once()
