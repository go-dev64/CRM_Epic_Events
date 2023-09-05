from crm_app.user.models.authentiction import Authentication
from crm_app.user.view.login_view import LoginView


class UserController:
    def __init__(self, session) -> None:
        self.session = session
        self.auth = Authentication(self.session)
        self.login_view = LoginView()

    def user_login(self):
        while True:
            try:
                msg = ""
                email, password = self.login_view.get_user_email_and_password(msg=msg)
                user = self.auth.login(email, password)
                if user is None:
                    raise Exception
            except Exception:
                msg = "Invalid Email or Password"

            else:
                return user
