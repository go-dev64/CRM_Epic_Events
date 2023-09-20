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
                assert seller_ctrl.create_new_customer(session=session) == "create_new_customer"
            elif choice == 2:
                assert seller_ctrl.create_new_event(session=session) == "create_new_event"
            else:
                pass
