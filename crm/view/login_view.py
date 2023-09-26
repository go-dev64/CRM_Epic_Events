# View module of user login.
from rich.console import Console
from rich import print as pprint
from rich.prompt import Prompt, IntPrompt
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
            email = Prompt.ask(":email:   Please enter your Email")
            if 5 < len(email) < 255:
                break
            pprint(":warning: [prompt.invalid]Invalid Email")

        return email

    def get_password(self):
        while True:
            password = Prompt.ask(
                ":key:  Please enter your password [cyan](must be at least 8 characters)", password=True
            )
            if len(password) >= 8:
                break
            pprint(":warning: [prompt.invalid]password too short")

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
