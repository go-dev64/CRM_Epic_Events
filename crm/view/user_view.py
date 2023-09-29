import argon2
from crm.models.users import User
from crm.view.generic_view import GenericView
from rich.console import Console, Group
from rich.prompt import Prompt, IntPrompt


class UserView:
    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.console = Console()

    def _get_user_password(self) -> str:
        """
        The function is used to obtain the passport via a user input.
        The function ask a confirm password.If confir is ok return password hashed.

        Returns:
            _type_(str): Hashed password.
        """
        while True:
            password = self.generic_view._input_password()
            password_confirm = Prompt.ask("Confirm your password:")
            if password_confirm != password:
                self.console.print("[prompt.invalid] Ouups your first password is different")
            else:
                break
        ph = argon2.PasswordHasher()
        return ph.hash(password=password)

    def get_user_info_view(
        self,
        department: str,
        current_user_name: str,
        section: str = "Create New Collaborator/Get Information",
    ) -> dict:
        """
        Function get inforations for create a new collaborator. The Department will get in other function.

        Args:
            section (str): Section information to display in header
            department (str): department name to display in header
            current_user_name(str): Current user name to display in header

        Returns:
            dict: a dictionnary with informations to create a collaborator,
            like that : dict:{
                "name": "user_name",
                "email_address": "user_mail",
                "phone_number": "0123565",
                "password: "Apassword@12"
                }
        """
        user_info = {}
        restrictions = [
            x for x in User().availables_attribue_list() if x.get("attribute_name") not in ["password", "department"]
        ]
        self.generic_view.header(department=department, current_user=current_user_name, section=section)
        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            user_info[attribute_name] = self.generic_view.string_form(restriction=restriction)
        user_info["password"] = self._get_user_password()
        return user_info
