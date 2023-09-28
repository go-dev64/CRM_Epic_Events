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
        # test should return a new address.
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
