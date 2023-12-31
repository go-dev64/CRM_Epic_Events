# utiliser setup et towdnown
import os
import jwt
import pytest
from dotenv import load_dotenv
from crm.models.authentication import Authentication
from crm.models.users import Manager

load_dotenv()

wright_parametre = [
    ("m@gmail.com", "manager", "password_manager"),
    ("s@gmail.com", "seller", "password_seller"),
    ("su@gmail.com", "supporter", "password_supporter"),
]
bad_email_parametre = [
    ("bad_mail", "manager", "password_manager"),
    ("bad_mail@gmail.com", "seller", "password_seller"),
    ("bad_mail@gmail.com", "supporter", "password_supporter"),
]

bad_password_parametre = [
    ("m@gmail.com", "manager", "bad"),
    ("s@gmail.com", "seller", "bad"),
    ("su@gmail.com", "supporter", "bad"),
]

bad_data_parametre = [
    ("toto", "manager", "bad"),
    ("ser@gmail.com", "seller", "bad"),
    ("supr@gmail.com", "supporter", "bad"),
]


class TestAuthentication:
    def _get_user(self, session, users, email):
        users
        auth = Authentication()
        user = auth.get_user_with_email(session=session, email=email)
        return user

    def _login(self, session, users, email, password):
        users
        auth = Authentication()
        user = auth.login(session=session, email=email, input_password=password)
        return user

    @pytest.mark.parametrize("email, user_name, password", wright_parametre)
    def test_get_user_with_wright_email(self, db_session, users, email, user_name, password):
        # Test should return User.name.
        with db_session as session:
            users
            user = self._get_user(session, users, email)
            assert user.name == user_name

    @pytest.mark.parametrize("email, user_name, password", bad_email_parametre)
    def test_get_user_with_bad_email(self, db_session, users, email, user_name, password):
        # Test should return User.name.
        with db_session:
            users
            user = self._get_user(db_session, users, email)
            assert user is None

    @pytest.mark.parametrize("email, user_name, password", wright_parametre)
    def test_login_with_right_data(self, db_session, users, email, user_name, password):
        # Test login should return User connected.
        with db_session:
            users
            user = self._login(db_session, users, email, password)
            assert user.name == user_name

    def test_get_token_after_login(self):
        # Test should return user with token which representing his information id, name and department.
        user_manager = Manager(name="manager", email_address="manager@gmail.com", phone_number="+0335651")
        auth = Authentication()
        user = auth.get_token(user=user_manager)
        assert user.token is not None

        user_token_excepted = {"sub": user.id, "name": user_manager.name, "department": user_manager.department}
        headers = jwt.get_unverified_header(user.token)
        user_token_decoded = jwt.decode(user.token, key=os.getenv("TOKEN_KEY"), algorithms=[headers["alg"]])
        assert user_token_excepted["department"] == user_token_decoded["department"]
        assert user_token_excepted["sub"] == user_token_decoded["sub"]
        assert user_token_excepted["name"] == user_token_decoded["name"]

    @pytest.mark.parametrize("email, user_name, password", bad_email_parametre)
    def test_login_with_wrong_email_and_good_password(self, db_session, users, email, user_name, password):
        # Test should return None with wrong email.
        user = self._login(db_session, users, email, password)
        assert user is None

    @pytest.mark.parametrize("email, user_name, password", bad_password_parametre)
    def test_login_with_wrong_password_and_good_email(self, db_session, users, email, user_name, password):
        # Test should return None with wrong password.
        user = self._login(db_session, users, email, password)
        assert user is False

    @pytest.mark.parametrize("email, user_name, password", bad_data_parametre)
    def test_login_with_wrong_data(self, db_session, users, email, user_name, password):
        # Test should return None with wrong data.
        user = self._login(db_session, users, email, password)
        assert user is None

    @Authentication.is_authenticated
    def _foo(self, *args, **kwargs):
        return True

    def test_decorator_is_authenticated(self, db_session, current_user_is_manager):
        # Test should return True if user have a valid token.
        with db_session as session:
            current_user_is_manager
            result_excepted = self._foo(session=session)
            assert result_excepted is True

    def test_decorator_is_authenticated_without_token(self, db_session, mocker):
        # Test should return None.
        with db_session as session:
            user_manager = Manager(name="manager", email_address="manager@gmail.com", phone_number="+0335651")
            user_manager.token = "xx"
            session.current_user = user_manager
            with pytest.raises(jwt.DecodeError):
                self._foo(session=session)

    def test__password_validator_with_good_password(
        self,
    ):
        password = "Abcdefgh@10"
        result = Authentication._password_validator(password)
        assert result is True

    @pytest.mark.parametrize(
        "password", [("bdsg"), ("abcdefgh@10"), ("Abcdefgh@"), ("Abcdefgh10"), ("Abcde fgh@10"), ("ABCDEFHH@10")]
    )
    def test___password_validator_with_good_password(self, password):
        result = Authentication._password_validator(password)
        assert result is None
