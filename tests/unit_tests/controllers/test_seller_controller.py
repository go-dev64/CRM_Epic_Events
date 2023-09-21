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
