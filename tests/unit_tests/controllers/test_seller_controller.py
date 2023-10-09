from datetime import datetime
import pytest
from sqlalchemy import select
from crm.controller.seller_controller import SellerController
from crm.models.customer import Customer
from crm.models.element_administratif import Address, Contract, Event
from crm.models.users import Seller
from crm.models.utils import Utils
from crm.view.generic_view import GenericView


class TestSellerController:
    def _count_number_of_element(self, session) -> tuple():
        """the function count number of element in session.

        Args:
            session (_type_): _description_

        Returns:
            tuple(int,int,int,int): number_customer, number_contract, number_event, number_address
        """
        number_contract = len(session.scalars(select(Contract)).all())
        number_customer = len(session.scalars(select(Customer)).all())
        number_event = len(session.scalars(select(Event)).all())
        number_address = len(session.scalars(select(Address)).all())
        return number_customer, number_contract, number_event, number_address

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test_create_new_element(self, db_session, users, current_user_is_seller, mocker, choice):
        # test check if the wright function is returned according to user's choise.
        with db_session as session:
            users
            current_user_is_seller
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 3]
            mock_create_new_customer = mocker.patch.object(SellerController, "create_new_customer")
            mock_create_new_event = mocker.patch.object(SellerController, "create_new_event")
            mock_address = mocker.patch.object(Utils, "create_new_address")

            SellerController().create_new_element(session=session)
            if choice == 0:
                mock_create_new_customer.assert_called_once()
            elif choice == 1:
                mock_create_new_event.assert_called_once()
            elif choice == 2:
                mock_address.assert_called_once()

    def test_create_new_costumer(self, db_session, users, current_user_is_seller, mocker):
        # test should return a new customer.
        with db_session as session:
            users
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.view.seller_view.SellerView.get_info_customer_view", return_value="customer_info")
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_create = mocker.patch.object(Seller, "create_new_customer")
            SellerController().create_new_customer(session=session)
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation succesfull!"
            )
            mock_create.assert_called_once()

    def test_create_new_costumer_with_no_confirm(self, db_session, users, current_user_is_seller, mocker):
        # test should return a new customer.
        with db_session as session:
            users
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.view.seller_view.SellerView.get_info_customer_view", return_value="customer_info")
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_create = mocker.patch.object(Seller, "create_new_customer")
            SellerController().create_new_customer(session=session)
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation Cancelled!"
            )
            mock_create.assert_not_called()

    def test_select_contract_of_event(self, db_session, users, current_user_is_seller, mocker):
        # test should return element of index list 1.
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user_without_event", return_value=element_list)
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=1)
            result = seller.select_contract_of_event(session=session)
            assert result == element_list[1]

    def test_select_contract_of_event_without_contract(self, db_session, users, current_user_is_seller, mocker):
        # test should return None with empty list..
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user_without_event", return_value=element_list)
            result = seller.select_contract_of_event(session=session)
            assert result == None

    def test_select_address_of_event(self, db_session, users, current_user_is_seller, mocker):
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.utils.Utils.select_address", return_value=element_list[1])
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=1)
            result = seller.select_address_of_event(session=session)
            assert result == element_list[1]

    def test_select_address_of_event_without_address(self, db_session, users, current_user_is_seller, mocker):
        # test should return None with empty list..
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.models.utils.Utils.select_address", return_value=None)
            mocker.patch("crm.models.utils.Utils.create_new_address", return_value="toto")
            mock_message = mocker.patch.object(GenericView, "no_data_message")
            result = seller.select_address_of_event(session=session)
            assert result == "toto"
            mock_message.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_get_addess_of_event(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            mock_create_new_customer = mocker.patch.object(SellerController, "select_address_of_event")
            mock_address = mocker.patch.object(Utils, "create_new_address")
            SellerController().get_address_of_event(session=session)
            if choice == 0:
                mock_create_new_customer.assert_called_once()
            elif choice == 1:
                mock_address.assert_called_once()

    def test_get_event_info(self, db_session, clients, current_user_is_seller, mocker):
        # test should return a info of event.
        with db_session as session:
            clients
            current_user_is_seller
            info_event = {
                "total_amount": 2133333,
                "remaining": 123,
                "signed_contract": True,
                "customer": "",
            }
            mocker.patch("crm.view.seller_view.SellerView.get_event_info_view", return_value=info_event)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.select_contract_of_event", return_value="contract"
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.get_address_of_event", return_value="address"
            )
            result = SellerController().get_event_info(session=session)
            assert result["total_amount"] == info_event["total_amount"]
            assert result["remaining"] == info_event["remaining"]
            assert result["signed_contract"] == info_event["signed_contract"]
            assert result["contract"] == "contract"
            assert result["address"] == "address"

    def test_create_new_event(self, db_session, contracts, address, events, current_user_is_seller, mocker):
        # test should return a new event in event list.
        with db_session as session:
            contract = contracts[0]
            address
            events
            current_user_is_seller
            event_info = {
                "name": "new_event",
                "date_start": datetime.now(),
                "date_end": datetime.now(),
                "attendees": 20,
                "note": "queles notes",
                "contract": contract,
                "supporter": None,
                "address": address,
            }
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.controller.seller_controller.SellerController.get_event_info", return_value=event_info)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_create = mocker.patch.object(Seller, "create_new_event")
            SellerController().create_new_event(session=session)
            mock_confirm.assert_called_once_with(
                section=" Create New event", session=session, msg="Operation succesfull!"
            )
            mock_create.assert_called_once()

    def test_create_new_event_no_comfirme(
        self, db_session, contracts, address, events, current_user_is_seller, mocker
    ):
        # test should return a new event in event list.
        with db_session as session:
            contract = contracts[0]
            address
            events
            current_user_is_seller
            event_info = {
                "name": "new_event",
                "date_start": datetime.now(),
                "date_end": datetime.now(),
                "attendees": 20,
                "note": "queles notes",
                "contract": contract,
                "supporter": None,
                "address": address,
            }
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.controller.seller_controller.SellerController.get_event_info", return_value=event_info)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_create = mocker.patch.object(Seller, "create_new_event")
            SellerController().create_new_event(session=session)
            mock_confirm.assert_called_once_with(
                section=" Create New event", session=session, msg="Operation Cancelled!"
            )
            mock_create.assert_not_called()

    def test_display_all_customers(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_customers", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_customers(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_customers_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_customers", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_customers(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_customers_of_user(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_clients_of_user", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_customersof_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_customers_of_userwith_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_clients_of_user", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_customersof_user(session=session)
            mock_display_elements.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_customer_type_to_display(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 2]
            mock_display_all_customers = mocker.patch.object(SellerController, "display_all_customers")
            mock_display_all_customersof_user = mocker.patch.object(SellerController, "display_all_customersof_user")
            SellerController().select_customer_type_to_display(session=session)
            if choice == 0:
                mock_display_all_customers.assert_called_once()
            elif choice == 1:
                mock_display_all_customersof_user.assert_called_once()

    def test_display_all_contracts(self, db_session, users, current_user_is_seller, mocker):
        # test should display contracts elements.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_contracts", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_contracts(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_seller
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_contracts", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_contracts(session=session)
            mock_display_elements.assert_called_once()

    def test_all_contracts_of_user(self, db_session, users, current_user_is_seller, mocker):
        # test should display contracts element.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SellerController().display_all_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_of_user_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # test should display no data msg.
        with db_session as session:
            users
            current_user_is_seller
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_unpayed_contracts_of_user(self, db_session, users, current_user_is_seller, mocker):
        # test should display contracts element.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_unpayed_contracts", return_value=element_list)
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
            element_list = []
            mocker.patch("crm.models.users.Seller.get_unpayed_contracts", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_unpayed_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_unsigned_contracts_of_user(self, db_session, users, current_user_is_seller, mocker):
        # test should display contracts element.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_unsigned_contracts", return_value=element_list)
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
            element_list = []
            mocker.patch("crm.models.users.Seller.get_unsigned_contracts", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_unsigned_contracts_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_contracts_of_user_without_event(self, db_session, users, current_user_is_seller, mocker):
        # test should display contracts element.
        with db_session as session:
            users
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user_without_event", return_value=element_list)
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
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user_without_event", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SellerController().display_all_contracts_of_user_without_event(session=session)
            mock_display_elements.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3), (4)])
    def test_select_contract_type_to_display(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 5]
            mock_display_all_contracts = mocker.patch.object(SellerController, "display_all_contracts")
            mock_display_all_contracts_of_user = mocker.patch.object(SellerController, "display_all_contracts_of_user")
            mock_display_all_unpayed_contracts_of_user = mocker.patch.object(
                SellerController, "display_all_unpayed_contracts_of_user"
            )
            mock_display_all_unsigned_contracts_of_user = mocker.patch.object(
                SellerController, "display_all_unsigned_contracts_of_user"
            )
            mock_display_all_contracts_of_user_without_event = mocker.patch.object(
                SellerController, "display_all_contracts_of_user_without_event"
            )
            SellerController().select_contract_type_to_display(session=session)
            if choice == 0:
                mock_display_all_contracts.assert_called_once()
            elif choice == 1:
                mock_display_all_contracts_of_user.assert_called_once()
            if choice == 2:
                mock_display_all_unpayed_contracts_of_user.assert_called_once()
            elif choice == 3:
                mock_display_all_unsigned_contracts_of_user.assert_called_once()
            elif choice == 4:
                mock_display_all_contracts_of_user_without_event.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test_select_element_type_to_be_updated(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 3]
            mock_update_seller_customer = mocker.patch.object(SellerController, "update_seller_customer")
            mock_update_seller_contract = mocker.patch.object(SellerController, "update_seller_contract")
            mock_update_address = mocker.patch.object(Utils, "update_address")

            SellerController().select_element_type_to_be_updated(session=session)
            if choice == 0:
                mock_update_seller_customer.assert_called_once()
            elif choice == 1:
                mock_update_seller_contract.assert_called_once()
            if choice == 2:
                mock_update_address.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_customer(self, db_session, users, clients, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            clients
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_clients_of_user", return_value=element_list)
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            result = SellerController().select_customer(session=session)
            assert result == element_list[choice]

    def test_select_customer_with_no_data(self, db_session, users, clients, current_user_is_seller, mocker):
        with db_session as session:
            users
            clients
            current_user_is_seller
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_clients_of_user", return_value=element_list)
            result = SellerController().select_customer(session=session)
            assert result == None

    @pytest.mark.parametrize(
        "attribute,new_value",
        [("name", "test"), ("email_address", "test@email"), ("phone_number", "test")],
    )
    def test_change_attribute_customer(
        self, db_session, users, clients, current_user_is_seller, mocker, attribute, new_value
    ):
        # test should to call a upadte function.
        with db_session as session:
            users
            clients
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_update = mocker.patch.object(Seller, "update_customer")
            SellerController().change_attribute_of_customer(
                session=session,
                section=" Create new Customer",
                attribute_selected=attribute,
                customer_selected=clients[0],
            )
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation succesfull!"
            )
            mock_update.assert_called_once()

    @pytest.mark.parametrize(
        "attribute,new_value", [("name", "test"), ("email_address", "test@email"), ("phone_number", "test")]
    )
    def test_change_attribute_customer_no_confirm(
        self, db_session, users, clients, current_user_is_seller, mocker, attribute, new_value
    ):
        # test should to return a confirm message to canceled operation..
        with db_session as session:
            users
            clients
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Seller, "update_customer")
            SellerController().change_attribute_of_customer(
                session=session,
                section=" Create new Customer",
                attribute_selected=attribute,
                customer_selected=clients[0],
            )
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation Cancelled!"
            )
            mock_update.assert_not_called()

    def test_change_email_address_customer(self, db_session, users, current_user_is_seller, clients, mocker):
        # test shoud return customer with new address.
        with db_session as session:
            users
            current_user_is_seller
            clients
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.view.seller_view.SellerView.get_customer_email", return_value="email")
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            SellerController().change_email_address(session=session, customer_selected=clients[0])
            assert clients[0].email_address == "email"
            mock_confirm.assert_called_once()

    def test_change_email_address_customer_with_no_data(
        self, db_session, users, current_user_is_seller, clients, mocker
    ):
        # test shoud return customer with new address.
        with db_session as session:
            users
            current_user_is_seller
            clients
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.view.seller_view.SellerView.get_customer_email", return_value="email")
            mock_mesage = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Seller, "update_customer")
            SellerController().change_email_address(session=session, customer_selected=clients[0])
            mock_mesage.assert_called_once()
            mock_update.assert_not_called()

    def test_update_seller_customer_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        # Test should retrun a msg no data.
        with db_session as session:
            users
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.controller.seller_controller.SellerController.select_customer", return_value=None)
            mock_mesage = mocker.patch.object(GenericView, "no_data_message")
            mock_change_attribute = mocker.patch.object(SellerController, "change_attribute_of_customer")
            seller.update_seller_customer(session=session)
            mock_mesage.assert_called_once_with(
                session=session, section="Update your Customer", msg="No customer available to updating!"
            )
            mock_change_attribute.assert_not_called()

    @pytest.mark.parametrize("attribute,new_value", [("name", "test"), ("phone_number", "test")])
    def test_update_seller_customer(
        self, db_session, clients, users, current_user_is_seller, mocker, attribute, new_value
    ):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            clients
            users
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.controller.seller_controller.SellerController.select_customer", return_value=clients[0])
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mock_change_attribute = mocker.patch.object(SellerController, "change_attribute_of_customer")
            seller.update_seller_customer(session=session)
            mock_change_attribute.assert_called_once()

    @pytest.mark.parametrize("attribute,new_value", [("email_address", "test@email")])
    def test_update_seller_customer_email(
        self, db_session, clients, users, current_user_is_seller, mocker, attribute, new_value
    ):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            clients
            users
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.controller.seller_controller.SellerController.select_customer", return_value=clients[0])
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mock_change_attribute = mocker.patch.object(SellerController, "change_email_address")
            seller.update_seller_customer(session=session)
            mock_change_attribute.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_contract(self, db_session, users, clients, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            clients
            current_user_is_seller
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user", return_value=element_list)
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=choice,
            )
            result = SellerController().select_contract(session=session)
            assert result == element_list[choice]

    def test_select_contract_with_no_data(self, db_session, users, current_user_is_seller, mocker):
        with db_session as session:
            users
            current_user_is_seller
            element_list = []
            mocker.patch("crm.models.users.Seller.get_all_contracts_of_user", return_value=element_list)
            result = SellerController().select_contract(session=session)
            assert result == None

    @pytest.mark.parametrize(
        "attribute,new_value", [("total_amount", 1233), ("remaining", 12), ("signed_contract", True)]
    )
    def test_change_attribute_contract(
        self, db_session, users, contracts, current_user_is_seller, attribute, new_value, mocker
    ):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            contract = contracts[0]
            current_user_is_seller
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            mock_update = mocker.patch.object(Seller, "update_contract")
            SellerController().change_attribute_of_contract(session=session, contract_selected=contract)
            mock_update.assert_called_once()
            mock_confirm.assert_called_once_with(
                session=session, section=" Upadte Contract", msg="Operation succesfull!"
            )

    @pytest.mark.parametrize(
        "attribute,new_value", [("total_amount", 1233), ("remaining", 12), ("signed_contract", True)]
    )
    def test_change_attribute_contract_no_confirm(
        self, db_session, users, contracts, current_user_is_seller, attribute, new_value, mocker
    ):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            contract = contracts[0]
            current_user_is_seller
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_update = mocker.patch.object(Seller, "update_contract")
            SellerController().change_attribute_of_contract(session=session, contract_selected=contract)
            mock_update.assert_not_called()
            mock_confirm.assert_called_once_with(
                session=session, section=" Upadte Contract", msg="Operation Cancelled!"
            )

    def test_update_seller_contract_with_no_data(self, db_session, users, contracts, current_user_is_seller, mocker):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            contracts
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.controller.seller_controller.SellerController.select_contract", return_value=None)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            seller.update_seller_contract(session=session)
            mock_confirm.assert_called_once_with(
                session=session, section=" Upadte Contract", msg="No contract available to updating!"
            )

    def test_update_seller_contract(self, db_session, users, contracts, current_user_is_seller, mocker):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            users
            contract = contracts[0]
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.controller.seller_controller.SellerController.select_contract", return_value=contract)
            mock_update = mocker.patch.object(SellerController, "change_attribute_of_contract")
            seller.update_seller_contract(session=session)
            mock_update.assert_called_once()
