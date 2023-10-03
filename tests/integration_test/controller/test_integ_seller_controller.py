from datetime import datetime
import pytest
from sqlalchemy import select
from crm.controller.seller_controller import SellerController
from crm.controller.manager_controller import ManagerController
from crm.models.users import Manager, Seller, Supporter, User, Event, Customer
from crm.view.generic_view import GenericView


class TestSellerController:
    def test_select_contract_of_event(self, db_session, users, contracts, current_user_is_seller, mocker):
        # test should return element of index list 1.
        with db_session as session:
            users
            contracts
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=0)
            result = seller.select_contract_of_event(session=session)
            assert result == contracts[0]

    def test_select_contract_of_event_without_contract(self, db_session, users, current_user_is_seller, mocker):
        # test should return None with empty list..
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            result = seller.select_contract_of_event(session=session)
            assert result == None

    def test_select_address_of_event(self, db_session, users, address, current_user_is_seller, mocker):
        with db_session as session:
            users
            address
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=0)
            result = seller.select_address_of_event(session=session)
            assert result == address

    def test_select_address_of_event_without_address(self, db_session, users, current_user_is_seller, mocker):
        # test should return None with empty list..
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.no_data_message", return_value="element_list")
            mocker.patch("crm.models.utils.Utils.create_new_address", return_value="toto")
            result = seller.select_address_of_event(session=session)
            assert result == "toto"

    def test_display_all_customers(self, db_session, users, clients, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            clients
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_customers(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_customers_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_customers(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_customers_of_user(self, db_session, users, clients, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            clients
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_customersof_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_customers_of_user_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_customersof_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts(self, db_session, users, contracts, current_user_is_seller, mocker):
        # test should display contracts elements.
        with db_session as session:
            users
            current_user_is_seller
            contracts
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_contracts(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_contracts(session=session)
            mock_display_elements.assert_called_once()

    def test_all_contracts_of_user(self, db_session, users, contracts, current_user_is_seller, mocker):
        # test should display contracts element.
        with db_session as session:
            users
            contracts
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_of_user_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display no data msg.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_unpayed_contracts_of_user(self, db_session, contracts, users, current_user_is_seller, mocker):
        # test should display contracts element.
        with db_session as session:
            users
            contracts
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_unpayed_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_unpayed_contracts_of_user_with_no_data(
        self, db_session, users, current_user_is_seller, mocker
    ):
        # test should display no data msg.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_unpayed_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_unsigned_contracts_of_user(
        self, db_session, users, contracts, current_user_is_seller, mocker
    ):
        # test should display contracts element.
        with db_session as session:
            users
            contracts
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_unsigned_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_unsigned_contracts_of_user_with_no_data(
        self, db_session, users, current_user_is_seller, mocker
    ):
        # test should display no data msg.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_unsigned_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_of_user_without_event(
        self, db_session, users, contracts, current_user_is_seller, mocker
    ):
        # test should display contracts element.
        with db_session as session:
            users
            contracts
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_contracts_of_user_without_event(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_of_user_without_event_with_no_data(
        self, db_session, users, current_user_is_seller, mocker
    ):
        # test should display no data msg.
        with db_session as session:
            users
            current_user_is_seller
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_contracts_of_user_without_event(session=session)
            mock_display_elements.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_customer(self, db_session, users, clients, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            clients
            current_user_is_seller
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            result = SellerController().select_customer(session=session)
            assert result == clients[choice]

    def test_select_customer_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        with db_session as session:
            users
            current_user_is_seller
            result = SellerController().select_customer(session=session)
            assert result == None

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_contract(self, db_session, users, clients, contracts, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            clients
            contracts
            current_user_is_seller
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            result = SellerController().select_contract(session=session)
            assert result == contracts[choice]

    def test_select_contract_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        with db_session as session:
            users

            current_user_is_seller
            result = SellerController().select_contract(session=session)
            assert result == None
