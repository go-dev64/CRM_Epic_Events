import pytest
from pytest_mock import mocker
from sqlalchemy import select
from crm.models.element_administratif import Address
from crm.models.utils import Utils


class TestUtils:
    def test_get_type_of_user_with_manager(self, db_session, users, current_user_is_manager):
        u = Utils()
        with db_session as session:
            users
            current_user_is_manager
            assert u.get_type_of_user(session.current_user) == "Manager"

    def test_get_type_of_user_with_seller(self, db_session, users, current_user_is_seller):
        u = Utils()
        with db_session as session:
            users
            current_user_is_seller
            assert u.get_type_of_user(session.current_user) == "Seller"

    def test_get_type_of_user_with_supporter(self, db_session, users, current_user_is_supporter):
        u = Utils()
        with db_session as session:
            users
            current_user_is_supporter
            assert u.get_type_of_user(session.current_user) == "Supporter"

    def test_create_new_address(self, db_session, users, current_user_is_user, address, mocker):
        u = Utils()
        with db_session as session:
            users
            address
            current_user_is_user
            address_info = {
                "number": 1,
                "street": "address_info",
                "city": "city",
                "postal_code": 135,
                "country": "country",
                "note": "note",
            }
            mocker.patch("crm.view.generic_view.GenericView.get_address_info", return_value=address_info)
            u.create_new_address(session=session)
            list_address = session.scalars(select(Address)).all()
            assert len(list_address) == 2

    """@pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_select_contract_attribute_to_be_updated(
        self, db_session, users, contracts, current_user_is_manager, mocker, choice
    ):
        # test should retrun a good attribure of cotract according a user's choice.
        with db_session as session:
            users
            contract = contracts[0]
            current_user_is_manager
            manager = ManagerController()
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=choice)
            if choice == 0:
                assert manager._select_contract_attribute_to_be_updated(contract) == "total_amount"
            elif choice == 1:
                assert manager._select_contract_attribute_to_be_updated(contract) == "remaining"
            elif choice == 2:
                assert manager._select_contract_attribute_to_be_updated(contract) == "signed_contract"
            elif choice == 3:
                assert manager._select_contract_attribute_to_be_updated(contract) == "customer"
"""
