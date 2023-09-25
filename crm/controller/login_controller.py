from crm.controller.manager_controller import ManagerController
from crm.models.authentication import Authentication
from crm.models.exceptions import EmailError, PasswordError
from crm.view.login_view import LoginView
import time


class LoginController:
    auth = Authentication()

    def __init__(self) -> None:
        self.login_view = LoginView()
        self.auth = Authentication()
        self.manager = ManagerController()

    def user_login(self, session):
        """
        Function enabling to log up a user.


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
                self.login_view.authentication_ok()
                time.sleep(2)
                return self.auth.get_token(user)
