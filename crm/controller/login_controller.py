from crm.controller.manager_controller import ManagerController
from crm.models.authentication import Authentication
from crm.models.exceptions import EmailError, PasswordError
from crm.view.login_view import LoginView


class LoginController:
    auth = Authentication()

    def __init__(self) -> None:
        self.login_view = LoginView()
        self.auth = Authentication()
        self.manager = ManagerController()

    def user_login(self, session):
        while True:
            try:
                msg = ""
                email, password = self.login_view.get_user_email_and_password(msg=msg)
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
                return self.auth.get_token(user)
