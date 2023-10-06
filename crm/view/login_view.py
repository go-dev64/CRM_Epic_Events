# View module of user login.
from email_validator import validate_email, EmailNotValidError
from rich.console import Console
from rich.prompt import Prompt
from crm.models.exceptions import PasswordError
from crm.view.generic_view import GenericView
from crm.models.authentication import Authentication


class LoginView:
    def __init__(self) -> None:
        self.console = Console()
        self.generic = GenericView()
        self.auth = Authentication()

    def authentication_ok(self):
        self.console.print("✅ Authentication is ok ✅")

    def get_email(self):
        while True:
            try:
                email = Prompt.ask(":email:   Please enter your Email")
                email_info = validate_email(email, check_deliverability=False)
                if 5 < len(email_info) < 255:
                    break
                self.console().print(":warning: [prompt.invalid]Invalid Email")
            except EmailNotValidError as e:
                self.console.print(e)

        return email_info.normalized

    def get_password(self):
        while True:
            try:
                password = Prompt.ask(
                    ":key:  Please enter your password [cyan](must be at least 8 characters)", password=True
                )

                if self.auth._password_validator(password) is None:
                    raise PasswordError()
            except PasswordError as msg:
                self.console().print(f"{msg}")
            else:
                break
        return password

    def get_user_email_and_password(self, msg=None):
        section = "Authentication"
        while True:
            self.generic.header(section=section)
            if msg != None:
                self.console.print(f":warning: {msg} :warning:")
            email = self.get_email()
            password = self.get_password()
            return email, password
