# utiliser setup et towdnown
import pytest
from crm_app.user.models.users import Manager, Seller, Supporter
from crm_app.user.models.authentiction import Authentication


class TestAuthentication:
    def _create_users(self, db_session, users):
        db_session.add_all(users)
        db_session.commit()

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("manager@gmail.com", "manager", "password_manager"),
            ("seller@gmail.com", "seller", "password_seller"),
            ("supporter@gmail.com", "supporter", "password_supporter"),
        ],
    )
    def test_login_with_right_email_and_password(self, db_session, users, email, user_name, password):
        self._create_users(db_session, users)
        auth = Authentication(db_session)
        user = auth.login(email=email, password=password)
        print(type(user))
        assert user.name == user_name

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("bad_mail", "manager", "password_manager"),
            ("bad_mail@gmail.com", "seller", "password_seller"),
            ("bad_mail@gmail.com", "supporter", "password_supporter"),
        ],
    )
    def test_login_with_wrong_email_and_good_password(self, db_session, users, email, user_name, password):
        self._create_users(db_session, users)
        auth = Authentication(db_session)
        user = auth.login(email=email, password=password)
        assert user == None

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("manager@gmail.com", "manager", "bad"),
            ("seller@gmail.com", "seller", "bad"),
            ("supporter@gmail.com", "supporter", "bad"),
        ],
    )
    def test_login_with_wrong_password_and_good_email(self, db_session, users, email, user_name, password):
        self._create_users(db_session, users)
        auth = Authentication(db_session)
        user = auth.login(email=email, password=password)
        assert user == None

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("toto", "manager", "bad"),
            ("ser@gmail.com", "seller", "bad"),
            ("supr@gmail.com", "supporter", "bad"),
        ],
    )
    def test_login_with_wrong_data(self, db_session, users, email, user_name, password):
        self._create_users(db_session, users)
        auth = Authentication(db_session)
        user = auth.login(email=email, password=password)
        assert user == None
