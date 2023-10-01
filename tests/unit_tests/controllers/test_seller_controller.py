from datetime import datetime
import pytest
from sqlalchemy import select
from crm.controller.seller_controller import SellerController
from crm.models.customer import Customer
from crm.models.element_administratif import Event
from crm.models.users import Seller


class TestSellerController:
    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test_create_new_element(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            seller_ctrl = SellerController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.create_new_customer",
                return_value="create_new_customer",
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.create_new_event", return_value="create_new_event"
            )
            mocker.patch("crm.models.utils.Utils.create_new_address", return_value="create_new_address")
            if choice == 0:
                assert seller_ctrl.create_new_element(session=session) == "create_new_customer"
            elif choice == 1:
                assert seller_ctrl.create_new_element(session=session) == "create_new_event"
            elif choice == 2:
                assert seller_ctrl.create_new_element(session=session) == "create_new_address"
            else:
                pass

    def test_create_new_costumer(self, db_session, clients, current_user_is_seller, mocker):
        # test should return a new customer.
        with db_session as session:
            clients
            current_user_is_seller
            customer_info = {
                "name": "toto le client",
                "email_address": "email@com",
                "phone_number": "+516184684",
                "company": "une company",
            }
            mocker.patch("crm.view.seller_view.SellerView.get_info_customer_view", return_value=customer_info)
            new_customer = SellerController().create_new_customer(session=session)
            list_customer = session.scalars(select(Customer)).all()
            assert len(list_customer) == 3
            assert new_customer.name == customer_info["name"]
            assert new_customer.email_address == customer_info["email_address"]
            assert new_customer.phone_number == customer_info["phone_number"]
            assert new_customer.company == customer_info["company"]
            assert new_customer.seller_contact == session.current_user

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

    def get_event_info(self, db_session, clients, current_user_is_seller, mocker):
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
            info = mocker.patch("crm.view.seller_view.SellerView.get_event_info_view", return_value=info_event)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.select_contract_of_event", return_value="toto"
            )
            result = Seller().get_event_info(session=session)
            assert result == info
            assert result["contract"] == "toto"

    def test_create_new_event(self, db_session, contracts, address, current_user_is_seller, mocker):
        # test should return a new event in event list.
        with db_session as session:
            contract = contracts[0]
            address = address
            current_user = current_user_is_seller
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
            mocker.patch("crm.controller.seller_controller.SellerController.get_event_info", return_value=event_info)

            new_event = SellerController().create_new_event(session=session)
            list_event = session.scalars(select(Event)).all()
            assert len(list_event) == 1
            assert new_event.name == event_info["name"]
            assert isinstance(new_event.date_start, datetime)
            assert isinstance(new_event.date_end, datetime)
            assert new_event.attendees == event_info["attendees"]
            assert new_event.note == event_info["note"]
            assert new_event.address == address

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_customer_type_to_display(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            seller_ctrl = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            mocker.patch("crm.view.generic_view.GenericView.display_table_of_elements", return_value=choice)
            if choice == 0:
                assert seller_ctrl.select_customer_type_to_display(session=session) == choice
            elif choice == 1:
                assert seller_ctrl.select_customer_type_to_display(session=session) == choice

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3), (4)])
    def test_select_contract_type_to_display(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            seller_ctrl = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            mocker.patch("crm.view.generic_view.GenericView.display_elements", return_value=choice)
            if choice == 0:
                assert seller_ctrl.select_contract_type_to_display(session=session) == choice
            elif choice == 1:
                assert seller_ctrl.select_contract_type_to_display(session=session) == choice
            elif choice == 2:
                assert seller_ctrl.select_contract_type_to_display(session=session) == choice
            elif choice == 3:
                assert seller_ctrl.select_contract_type_to_display(session=session) == choice
            elif choice == 4:
                assert seller_ctrl.select_contract_type_to_display(session=session) == choice

    @pytest.mark.parametrize("choice", [(0), (1), (2)])
    def test_select_element_type_to_be_updated(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            current_user_is_seller
            seller_ctrl = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.update_seller_customer",
                return_value="update_customer",
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.update_seller_contract",
                return_value="updat_contract",
            )
            mocker.patch("crm.models.utils.Utils.update_address", return_value="update_address")
            if choice == 0:
                assert seller_ctrl.select_element_type_to_be_updated(session=session) == "update_customer"
            elif choice == 1:
                assert seller_ctrl.select_element_type_to_be_updated(session=session) == "updat_contract"
            elif choice == 2:
                assert seller_ctrl.select_element_type_to_be_updated(session=session) == "update_address"

    @pytest.mark.parametrize(
        "attribute,new_value",
        [("name", "test"), ("email_address", "test@email"), ("phone_number", "test"), ("password", "test")],
    )
    def test_update_seller_customer(
        self, db_session, clients, users, current_user_is_seller, mocker, attribute, new_value
    ):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            clients
            users
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.models.utils.Utils._select_element_in_list", return_value=clients[0])
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            seller.update_seller_customer(session=session)
            assert getattr(clients[0], attribute) == new_value

    @pytest.mark.parametrize(
        "attribute,new_value", [("total_amount", 1233), ("remaining", 12), ("signed_contract", True)]
    )
    def test_update_seller_customer(
        self, db_session, clients, users, contracts, current_user_is_seller, mocker, attribute, new_value
    ):
        # Test should retrun a event with supporter updated.
        with db_session as session:
            clients
            users
            contracts
            current_user_is_seller
            seller = SellerController()
            mocker.patch("crm.models.utils.Utils._select_element_in_list", return_value=contracts[0])
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            seller.update_seller_contract(session=session)
            assert getattr(contracts[0], attribute) == new_value
