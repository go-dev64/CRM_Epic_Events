from datetime import datetime
import pytest
from sqlalchemy import select
from crm.controller.seller_controller import SellerController
from crm.controller.manager_controller import ManagerController
from crm.models.element_administratif import Address, Contract
from crm.models.users import Manager, Seller, Supporter, User, Event, Customer
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

    def test_create_new_costumer(self, db_session, users, current_user_is_seller, mocker):
        # test should return a new customer.
        with db_session as session:
            users
            current_user_is_seller
            customer_info = {
                "name": "toto le client",
                "email_address": "email@com",
                "phone_number": "+516184684",
                "company": "une company",
            }
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.view.seller_view.SellerView.get_info_customer_view", return_value=customer_info)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")

            number_customer_before = self._count_number_of_element(session)[0]
            new_customer = SellerController().create_new_customer(session=session)
            number_customer = self._count_number_of_element(session)[0]
            # number of customer +1
            assert number_customer == number_customer_before + 1
            assert new_customer.name == customer_info["name"]
            assert new_customer.email_address == customer_info["email_address"]
            assert new_customer.phone_number == customer_info["phone_number"]
            assert new_customer.company == customer_info["company"]
            assert new_customer.seller_contact == session.current_user
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation succesfull!"
            )

    def test_create_new_costumer_with_no_confirm(self, db_session, users, current_user_is_seller, mocker):
        # test should return a new customer.
        with db_session as session:
            users
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.view.seller_view.SellerView.get_info_customer_view", return_value="customer_info")
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            mock_create = mocker.patch.object(Seller, "create_new_customer")
            number_customer_before = self._count_number_of_element(session)[0]
            SellerController().create_new_customer(session=session)
            number_customer = self._count_number_of_element(session)[0]
            assert number_customer == number_customer_before
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation Cancelled!"
            )
            mock_create.assert_not_called()

    def test_select_contract_of_event(self, db_session, users, contracts, current_user_is_seller, mocker):
        # test should return element of index list 1.
        with db_session as session:
            users
            current_user_is_seller
            contracts
            seller = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=0)
            result = seller.select_contract_of_event(session=session)
            assert isinstance(result, Contract) == True

    def test_create_new_event(self, db_session, users, contracts, address, current_user_is_seller, mocker):
        # test should return a new event in event list.
        with db_session as session:
            users
            current_user_is_seller
            contract = contracts[0]
            address
            event_info = {
                "name": "new_event",
                "date_start": datetime.now(),
                "date_end": datetime.now(),
                "attendees": 20,
                "note": "queles notes",
                "address": address,
                "contract": contract,
                "supporter": None,
            }
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=True)
            mocker.patch("crm.controller.seller_controller.SellerController.get_event_info", return_value=event_info)
            mock_confirm = mocker.patch.object(GenericView, "confirmation_msg")
            number_event_before = self._count_number_of_element(session)[2]
            new_event = SellerController().create_new_event(session=session)
            number_event = self._count_number_of_element(session)[2]
            assert new_event.name == "new_event"
            assert number_event == number_event_before + 1
            assert isinstance(new_event.date_start, datetime)
            assert isinstance(new_event.date_end, datetime)
            assert new_event.attendees == 20
            assert new_event.note == "queles notes"
            assert new_event.address == address
            mock_confirm.assert_called_once_with(
                section=" Create New event", session=session, msg="Operation succesfull!"
            )

    def test_create_new_event_no_confirme(self, db_session, users, contracts, address, current_user_is_seller, mocker):
        # test should return a new event in event list.
        with db_session as session:
            users
            current_user_is_seller
            contract = contracts[0]
            address
            event_info = {
                "name": "new_event",
                "date_start": datetime.now(),
                "date_end": datetime.now(),
                "attendees": 20,
                "note": "queles notes",
                "address": address,
                "contract": contract,
                "supporter": None,
            }
            mocker.patch("crm.view.generic_view.GenericView.ask_comfirmation", return_value=False)
            mocker.patch("crm.controller.seller_controller.SellerController.get_event_info", return_value=event_info)
            mock_confirm = mocker.patch.object(GenericView, "no_data_message")
            number_event_before = self._count_number_of_element(session)[2]
            new_event = SellerController().create_new_event(session=session)
            number_event = self._count_number_of_element(session)[2]
            assert number_event == number_event_before
            mock_confirm.assert_called_once_with(
                section=" Create New event", session=session, msg="Operation Cancelled!"
            )

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

    def test_select_customer(self, db_session, users, clients, current_user_is_seller, mocker):
        with db_session as session:
            users
            clients
            current_user_is_seller
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=0,
            )
            result = SellerController().select_customer(session=session)
            assert result == clients[0]

    def test_select_customer_with_no_data(self, db_session, users, current_user_is_seller):
        with db_session as session:
            users
            current_user_is_seller
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
            SellerController().change_attribute_of_customer(
                session=session,
                section=" Create new Customer",
                attribute_selected=attribute,
                customer_selected=clients[0],
            )
            assert getattr(clients[0], attribute) == new_value
            mock_confirm.assert_called_once_with(
                section=" Create new Customer", session=session, msg="Operation succesfull!"
            )

    @pytest.mark.parametrize(
        "attribute,new_value",
        [("name", "test"), ("email_address", "test@email"), ("phone_number", "test")],
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

    def test_select_contract(self, db_session, users, contracts, current_user_is_seller, mocker):
        with db_session as session:
            users
            current_user_is_seller
            contracts
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=0)
            result = SellerController().select_contract(session=session)
            assert result == contracts[0]

    def test_select_contract_with_no_data(self, db_session, users, current_user_is_seller):
        with db_session as session:
            users
            current_user_is_seller
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
            SellerController().change_attribute_of_contract(session=session, contract_selected=contract)
            assert getattr(contract, attribute) == new_value
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
