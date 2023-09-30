from datetime import datetime
import pytest
from sqlalchemy import select
from crm.controller.seller_controller import SellerController
from crm.controller.manager_controller import ManagerController
from crm.models.users import Manager, Seller, Supporter, User, Event, Customer


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
