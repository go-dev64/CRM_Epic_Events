from crm.models.authentication import Authentication
from crm.models.exceptions import EmailError, PasswordError
from crm.models.users import User
from crm.models.utils import Utils
from crm.view.login_view import LoginView
import time


class LoginController:
    auth = Authentication()

    def __init__(self) -> None:
        self.login_view = LoginView()
        self.auth = Authentication()

    def user_login(self, session):
        """
        Function enabling to log up a user and pass like main user of session.

        Raises:
            EmailError: If email is invalid or unknow.
            PasswordError: Invalid password.

        Returns:
            _type_: user with proof of authentication (token).
        """
        msg = None
        while True:
            email, password = self.login_view.get_user_email_and_password(msg=msg)
            try:
                user = self.auth.login(session, email, password)
                if user is None:
                    raise EmailError()
                elif user is False:
                    raise PasswordError()
            except EmailError as error_mesage:
                msg = error_mesage
            except PasswordError as error_mesage:
                msg = error_mesage

            else:
                return user

    def define_main_user_of_session(self, session, user_connected: User) -> None:
        """The fonction define the main user session and this department.

        Args:
            session (_type_): _description_
            user_connected (User): User connected.
        """
        main_user = self.auth.get_token(user_connected)
        session.current_user = main_user
        session.current_user_department = Utils().get_type_of_user(user=main_user)
        self.login_view.authentication_ok()
        time.sleep(2)
