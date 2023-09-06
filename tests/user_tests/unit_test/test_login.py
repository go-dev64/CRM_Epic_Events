# utiliser setup et towdnown
import jwt
import pytest
from crm_app.user.models.users import Manager, Seller, Supporter
from crm_app.user.models.authentiction import Authentication, TOKEN_KEY


class TestAuthentication:
    def _create_users(self, session, users):
        # Create users for test.
        session.add_all(users)
        session.commit()

    def _get_user(self, db_session, users, email, user_name):
        with db_session as session:
            self._create_users(session, users)
            auth = Authentication()
            user = auth.get_user_with_email(session=session, email=email)
            return user

    def _login(self, db_session, users, email, user_name, password):
        with db_session as session:
            self._create_users(session, users)
            auth = Authentication()
            user = auth.login(db_session=session, email=email, input_password=password)
            return user

    @pytest.mark.parametrize(
        "email, user_name",
        [
            ("manager@gmail.com", "manager"),
            ("seller@gmail.com", "seller"),
            ("supporter@gmail.com", "supporter"),
        ],
    )
    def test_get_user_with_wright_email(self, db_session, users, email, user_name):
        # Test should return User.name.
        user = self._get_user(db_session, users, email, user_name)
        assert user.name == user_name

    @pytest.mark.parametrize(
        "email, user_name",
        [
            ("bad_mail", "manager"),
            ("bad_mail@gmail.com", "seller"),
            ("bad_mail@gmail.com", "supporter"),
        ],
    )
    def test_get_user_with_bad_email(self, db_session, users, email, user_name):
        # Test should return User.name.
        user = self._get_user(db_session, users, email, user_name)
        assert user == None

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("manager@gmail.com", "manager", "password_manager"),
            ("seller@gmail.com", "seller", "password_seller"),
            ("supporter@gmail.com", "supporter", "password_supporter"),
        ],
    )
    def test_login_with_right_data(self, db_session, users, email, user_name, password):
        # Test login should return User connected.
        user = self._login(db_session, users, email, user_name, password)
        assert user.name == user_name

    def test_get_token_after_login(self):
        user_manager = Manager(name="manager", email_address="manager@gmail.com", phone_number="+0335651")
        auth = Authentication()
        user = auth.get_token(user=user_manager)
        assert user.token is not None
        user_token_excepted = {"sub": user.id, "name": user_manager.name, "department": user_manager.department}
        headers = jwt.get_unverified_header(user.token)
        user_token_decoded = jwt.decode(user.token, key=TOKEN_KEY, algorithms=[headers["alg"]])
        assert user_token_excepted == user_token_decoded

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("bad_mail", "manager", "password_manager"),
            ("bad_mail@gmail.com", "seller", "password_seller"),
            ("bad_mail@gmail.com", "supporter", "password_supporter"),
        ],
    )
    def test_login_with_wrong_email_and_good_password(self, db_session, users, email, user_name, password):
        # Test should return None with wrong email.
        user = self._login(db_session, users, email, user_name, password)
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
        # Test should return None with wrong password.
        user = self._login(db_session, users, email, user_name, password)
        assert user == False

    @pytest.mark.parametrize(
        "email, user_name, password",
        [
            ("toto", "manager", "bad"),
            ("ser@gmail.com", "seller", "bad"),
            ("supr@gmail.com", "supporter", "bad"),
        ],
    )
    def test_login_with_wrong_data(self, db_session, users, email, user_name, password):
        # Test should return None with wrong data.
        user = self._login(db_session, users, email, user_name, password)
        assert user == None
