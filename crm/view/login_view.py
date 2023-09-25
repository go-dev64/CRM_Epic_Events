# View module of user login.
from rich.console import Console
from crm.view.generic_view import GenericView


class LoginView:
    def __init__(self) -> None:
        self.console = Console()
        self.generic = GenericView()

    def authentication_ok(self):
        self.console.print("✅ Authentication is ok ✅")

    def get_user_email_and_password(self, msg=None):
        section = "[i]Authentication[i]"
        while True:
            self.generic.header(section=section)
            if msg != None:
                self.console.print(f":warning: {msg} :warning:")
            email = self.console.input(":email:  Please, enter your email:")
            password = self.console.input(":key: Please, enter your Password: ")
            try:
                assert 5 < len(email) < 50
            except AssertionError:
                msg = "Email trop long ❌"

            else:
                return email, password
