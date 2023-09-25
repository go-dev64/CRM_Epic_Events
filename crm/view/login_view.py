# View module of user login.
from rich.console import Console
from rich import print
from crm.view.generic_view import GenericView
from rich.panel import Panel


class LoginView:
    def __init__(self) -> None:
        self.console = Console()
        self.generic = GenericView()

    def email(self):
        email = input("Your email: ")

    def get_user_email_and_password(self, msg=""):
        section = "[i]Authentication[i]"
        while True:
            self.generic.header(section=section)
            self.console.print(msg)
            email = input("Your email: ")
            password = input("Your Password: ")
            try:
                assert len(email) < 2
            except AssertionError:
                msg = "Email trop long ❌"

            else:
                return email, password
