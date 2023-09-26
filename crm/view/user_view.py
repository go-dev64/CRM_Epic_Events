from crm.view.generic_view import GenericView
from rich.console import Console, Group
from rich.prompt import Prompt, IntPrompt


class UserView:
    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.console = Console()

    def _get_userr_name(self):
        while True:
            name = Prompt.ask("Entrer name of collaborator:")
            if 5 > len(name):
                print(print("[prompt.invalid]Name too short"))
            elif len(name) > 40:
                print(print("[prompt.invalid]Name too long"))
            else:
                break
        return name

    def user_formulaire(self):
        while True:
            name = Prompt.ask()

    def get_user_info_view(self, section: str, department: str, current_user_name: str) -> dict:
        user_info = {}
        self.generic_view.header(department=department, current_user=current_user_name, section=section)
        user_info = {}
        return user_info
