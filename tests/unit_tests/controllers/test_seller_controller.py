import pytest
from crm.controller.seller_controller import SellerController


class TestSellerController:
    @pytest.mark.parametrize("choice", [(1), (2)])
    def test_create_new_element(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            seller_ctrl = SellerController()

            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.create_new_customer",
                return_value="create_new_customer",
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.create_new_event",
                return_value="create_new_event",
            )
            if choice == 1:
                assert seller_ctrl.create_new_element(session=session) == "create_new_customer"
            elif choice == 2:
                assert seller_ctrl.create_new_element(session=session) == "create_new_event"
            else:
                pass

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_customer_type_to_display(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            users
            current_user_is_seller
            seller_ctrl = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch("crm.view.generic_view.GenericView.display_element", return_value=choice)
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
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch("crm.view.generic_view.GenericView.display_element", return_value=choice)
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

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_select_element_type_to_be_updated(self, db_session, users, current_user_is_seller, mocker, choice):
        with db_session as session:
            current_user_is_seller
            seller_ctrl = SellerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            mocker.patch(
                "crm.controller.seller_controller.SellerController.update_seller_customer",
                return_value="update_customer",
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController.update_seller_contract",
                return_value="updat_contract",
            )
            if choice == 0:
                assert seller_ctrl.select_element_type_to_be_updated(session=session) == "update_customer"
            elif choice == 1:
                assert seller_ctrl.select_element_type_to_be_updated(session=session) == "updat_contract"

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
            mocker.patch(
                "crm.controller.seller_controller.SellerController._select_customer",
                return_value=clients[0],
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController._select_attribute_of_customer",
                return_value=attribute,
            )
            mocker.patch(
                "crm.controller.seller_controller.SellerController._get_new_value_of_attribute",
                return_value=new_value,
            )
            seller.update_seller_customer(session=session)
