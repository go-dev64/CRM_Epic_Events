from rich import print
from rich.console import Console, Group
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, Confirm
from rich.text import Text

from crm.models.authentication import Authentication
from crm.models.element_administratif import Address


class GenericView:
    RUN = True

    def __init__(self) -> None:
        self.console = Console()

    def set_section(self, section: str) -> Text:
        # function define the section to display (example: Home page).
        return Text.assemble(("Section:", "green bold"), (f"{section}", "bold"), justify="center")

    def set_department(self, department: str) -> Text:
        # function define the department to display (example: Department of Manager).
        return Text.assemble(("Department:", "blue bold"), (f"{department}", "bold"), justify="center")

    def set_current_user(self, current_user: str) -> Text:
        # function define the user connected to display (example: Seller 1).
        return Text.assemble(("User Connected:", "yellow bold"), (f"{current_user}", "blod"), justify="center")

    def set_element_renderable(self, section: Text, department: Text, current_user: Text) -> list[Panel]:
        """Function return list of Panel of elements with own style.

        Args:
            section (Text): Section to display.
            department (Text): Department to display.
            current_user (Text): User connected to display.

        Returns:
            list[Panel]: List of Panel for displaying.
        """
        display_section = self.set_section(section)
        display_department = self.set_department(department)
        user = self.set_current_user(current_user=current_user)
        elements = [display_section, display_department, user]
        elements_renderables = [Panel(element, border_style="blue") for element in elements]
        return elements_renderables

    def header(self, department: str = "", current_user: str = "", section: str = ""):
        """Function display header of application with Section , department and user connected.

        Args:
            department (str, optional): Department of usr connected. Defaults to "".
            current_user (str, optional): User connected. Defaults to "".
            section (str, optional): Section (exemple :Home page, Creating Contract). Defaults to "".
        """
        self.console.print("\033c", end="")  # Efface la page précédente
        app = Panel(Text("CRM Epic Event", style="Bold italic", justify="center"), border_style="blue")
        elements_renderables = self.set_element_renderable(
            department=department, current_user=current_user, section=section
        )
        self.console.print(app)
        self.console.print(Columns(elements_renderables, expand=True))

    def display_element_list(self, section: str, department: str, current_user_name: str, list_element: list):
        """Function display each element from list in Panel.

        Args:
            section (str): function header information. Actual section
            department (str): function header information. user's connected department
            current_user_name (str): function header information. user's connected Name
            list_element (list): list to display.
        """
        header = self.header(section=section, department=department, current_user=current_user_name)
        self.console.print(header)
        for i in range(len(list_element)):
            self.console.print(Panel(Text(f"{i} - {list_element[i]}", justify="center")))

    def display_element(self, list_element, restriction):
        element = self.select_element_view(list_element)
        print(element)
        return element

    def select_element_view(self, section: str, department: str, current_user_name: str, list_element: list) -> int:
        """The Function is used to select a element in list, the element index is returned.
        The header and elements list will be to display.

        Args:
            section (str): Section information to display in header
            department (str): department name to display in header
            current_user_name(str): Currentu ser name to display in header
            list_element (list): List of element to display

        Returns:
            int: Index of element selected.
        """
        self.display_element_list(
            section=section, department=department, current_user_name=current_user_name, list_element=list_element
        )
        range_list = len(list_element)
        while self.RUN:
            result = IntPrompt.ask(
                f" Enter a number between [b]1[/b] and [b]{range_list}[/b]",
            )
            if result >= 1 and result <= range_list:
                break
            self.console.print(f":pile_of_poo: [prompt.invalid]Number must be between 1 and {range_list}")
        return result - 1

    def get_address_info_view(
        self, department: str, current_user_name: str, section: str = "Create new address/Get Information"
    ) -> dict:
        """Function is used to get information create a new address.

        Args:
            department (str): Department information to display in header.
            current_user_name (str): Name of current user to display in header.
            section (str, optional): Info to display in header. Defaults to "Create new address/Get Information".

        Returns:
            dict: dict with info of new address.
        """
        address_info = {}
        restrictions = Address().availables_attribue_list()
        self.header(department=department, current_user=current_user_name, section=section)
        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            if restriction["parametre"]["type"] == str:
                address_info[attribute_name] = self.string_form(restriction=restriction)
            elif restriction["parametre"]["type"] == int:
                address_info[attribute_name] = self.integer_form(restriction=restriction)
            elif restriction["parametre"]["type"] == bool:
                address_info[attribute_name] = self.bool_form(restriction=restriction)
        return address_info

    def string_form(self, restriction: dict) -> str:
        """
        Function of form to input string.

        Args:
            restriction (dict): Restriction to input. Number max of caractere, etc.
            example:{"attribute_name": "name", "parametre": {"type": str, "max": 50}}

        Returns:
            str: input of user rspected restriction.
        """
        attribute_name = restriction["attribute_name"]
        condition_restriction = restriction["parametre"]["max"]
        if condition_restriction is None:
            condition_restriction = 2048
        while self.RUN:
            element_string = Prompt.ask(f"Entrer  {attribute_name}:")
            if len(element_string) < restriction["parametre"]["max"]:
                break
            self.console.print(f"[prompt.invalid]{attribute_name} too long")

        return element_string

    def integer_form(self, restriction: dict) -> int:
        condition_restriction = restriction["parametre"]["max"]
        if condition_restriction is None:
            condition_restriction = 9999999
        while self.RUN:
            result = IntPrompt.ask(f":rocket: Enter a number between [b]0[/b] and [b]{condition_restriction}[/b]")
            if result >= 0 and result <= condition_restriction - 1:
                break
            self.console.print(f"[prompt.invalid]Number must be between 0 and {condition_restriction}")
        return result

    def bool_form(self) -> bool:
        if Confirm.ask("Contract is signed?", default=True):
            return True
        else:
            return False

    def _input_password(self) -> str:
        """
        Function get input password by user, and check validity of password.

        Returns:
            _type_(str): password entered by user if validity is ok.
        """
        while True:
            password = Prompt.ask("Entrer your password:")
            if Authentication()._password_validator(password) is None:
                self.console.print(
                    "[prompt.invalid]Invalid password, password must contain:\n"
                    "Minimum 8 characters, one should be of Upper Case, special charatere and number between 0-9"
                )
            else:
                break
        return password
