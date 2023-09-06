# utiliser setup et towdnown
import jwt
import pytest
from crm_app.user.models.users import Manager, Seller, Supporter
from crm_app.user.models.authentiction import Authentication, TOKEN_KEY

wright_parametre = [
    ("manager@gmail.com", "manager", "password_manager"),
    ("seller@gmail.com", "seller", "password_seller"),
    ("supporter@gmail.com", "supporter", "password_supporter"),
]
bad_email_parametre = [
    ("bad_mail", "manager", "password_manager"),
    ("bad_mail@gmail.com", "seller", "password_seller"),
    ("bad_mail@gmail.com", "supporter", "password_supporter"),
]

bad_password_parametre = [
    ("manager@gmail.com", "manager", "bad"),
    ("seller@gmail.com", "seller", "bad"),
    ("supporter@gmail.com", "supporter", "bad"),
]

bad_data_parametre = [
    ("toto", "manager", "bad"),
    ("ser@gmail.com", "seller", "bad"),
    ("supr@gmail.com", "supporter", "bad"),
]

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOm51bGwsIm5hbWUiOiJtYW5hZ2VyIiwiZGVwYXJ0bWVudCI6Im1hbmFnZXJfdGFibGUifQ.QmrHhpbG59Tu4RmzG4q5ZkQ6RCqvxrHoIQZ4j5CMcWY"


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

    @pytest.mark.parametrize("email, user_name, password", wright_parametre)
    def test_get_user_with_wright_email(self, db_session, users, email, user_name, password):
        # Test should return User.name.
        user = self._get_user(db_session, users, email, user_name)
        assert user.name == user_name

    @pytest.mark.parametrize("email, user_name, password", bad_email_parametre)
    def test_get_user_with_bad_email(self, db_session, users, email, user_name, password):
        # Test should return User.name.
        user = self._get_user(db_session, users, email, user_name)
        assert user == None

    @pytest.mark.parametrize("email, user_name, password", wright_parametre)
    def test_login_with_right_data(self, db_session, users, email, user_name, password):
        # Test login should return User connected.
        user = self._login(db_session, users, email, user_name, password)
        assert user.name == user_name

    def test_get_token_after_login(self):
        # Test should return user with token which representing his information id, name and department.
        user_manager = Manager(name="manager", email_address="manager@gmail.com", phone_number="+0335651")
        auth = Authentication()
        user = auth.get_token(user=user_manager)
        assert user.token is not None
        user_token_excepted = {"sub": user.id, "name": user_manager.name, "department": user_manager.department}
        headers = jwt.get_unverified_header(user.token)
        user_token_decoded = jwt.decode(user.token, key=TOKEN_KEY, algorithms=[headers["alg"]])
        assert user_token_excepted == user_token_decoded

    def test_decode_token(self):
        # test valid info of token.
        auth = Authentication()
        user_token_decoded = auth.decode_token(TOKEN)
        user_data_excepted = {"sub": None, "name": "manager", "department": "manager_table"}
        assert user_data_excepted == user_token_decoded

    def test_decode_token_with_bad_key(self):
        # test should return None with wrong key.
        auth = Authentication()
        user_token_decoded = auth.decode_token(TOKEN, token_key="toto")
        assert user_token_decoded == None

    @pytest.mark.parametrize("email, user_name, password", bad_email_parametre)
    def test_login_with_wrong_email_and_good_password(self, db_session, users, email, user_name, password):
        # Test should return None with wrong email.
        user = self._login(db_session, users, email, user_name, password)
        assert user == None

    @pytest.mark.parametrize("email, user_name, password", bad_password_parametre)
    def test_login_with_wrong_password_and_good_email(self, db_session, users, email, user_name, password):
        # Test should return None with wrong password.
        user = self._login(db_session, users, email, user_name, password)
        assert user == False

    @pytest.mark.parametrize("email, user_name, password", bad_data_parametre)
    def test_login_with_wrong_data(self, db_session, users, email, user_name, password):
        # Test should return None with wrong data.
        user = self._login(db_session, users, email, user_name, password)
        assert user == None
