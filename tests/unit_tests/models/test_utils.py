import pytest
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
