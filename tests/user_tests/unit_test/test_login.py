# utiliser setup et towdnown
import pytest
from crm_app.user.models.users import Manager, Seller, Supporter
from crm_app.user.models.authentiction import Authentication


class TestAuthentication:
    def _create_users(self, db_session, users):
        db_session.add_all(users)
        db_session.commit()

    @pytest.mark.parametrize(
        "email, user_name",
        [
            ("manager@gmail.com", "manager"),
            ("seller@gmail.com", "seller"),
            ("supporter@gmail.com", "supporter"),
        ],
    )
    def test_find_user_with_right_email(self, db_session, users, email, user_name):
        self._create_users(db_session, users)
        auth = Authentication(db_session)
        user = auth.find_user_with_email(email=email)
        assert user.name == user_name

    def test_find_user_with_wrong_email(self, db_session, users):
        self._create_users(db_session, users)
        auth = Authentication(db_session)
        user = auth.find_user_with_email(email="toto@gmail.fr")
        assert user == None
