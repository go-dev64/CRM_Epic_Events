import argon2
from crm.models.authentication import Authentication
from crm.models.exceptions import EmailUniqueError
from crm.models.users import User
from crm.view.generic_view import GenericView
from rich.console import Console
from rich.prompt import Prompt

from crm.view.login_view import LoginView


class UserView:
    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.console = Console()
        self.login_view = LoginView()

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

    def _get_email(self, session) -> str:
        while True:
            try:
                email = self.login_view.get_email()
                if Authentication().get_user_with_email(session=session, email=email) is not None:
                    raise EmailUniqueError()
            except EmailUniqueError as msg:
                self.generic_view.console.print(msg)
            else:
                break
        return email

    def get_user_info_view(
        self,
        session,
        section: str = "Create New Collaborator/Get Information",
    ) -> dict:
        """
        Function get inforations for create a new collaborator. The Department will get in other function.

        Args:
            session: session sqlalchemy.
            section (str): Section information to display in header

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
            x
            for x in User().availables_attribue_list()
            if x.get("attribute_name") not in ["password", "email_address", "department"]
        ]
        self.generic_view.header(
            department=session.current_user_department, current_user=session.current_user.name, section=section
        )

        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            user_info[attribute_name] = self.generic_view.string_form(restriction=restriction)
        user_info["email_address"] = self._get_email(session=session)
        user_info["password"] = self._get_user_password()
        return user_info
