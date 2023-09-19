from crm.controller.manager_controller import ManagerController
from crm.models.authentication import Authentication
from crm.view.login_view import LoginView


class LoginController:
    auth = Authentication()

    def __init__(self, session) -> None:
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
            except EmailError:
                msg = "Invalid Email!"
            except PasswordError:
                msg = "Invalid Password!"

            else:
                return self.auth.get_token(user)

    @auth.is_authenticated
    def redirect_user_home_page(self, session):
        match type(session.current_user).__name__:
            case "Manager":
                self.manager_home_page(session=session)
            case "Seller":
                seller_home_page(session=session)
            case "Supporter":
                supporter_home_page(session=session)
