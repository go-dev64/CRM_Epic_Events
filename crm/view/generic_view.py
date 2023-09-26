from rich import print
from rich.console import Console, Group
from rich.columns import Columns
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text


class GenericView:
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
        """
        Function return list of Panel of elements with own style.

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
        """
        Function display header of application with Section , department and user connected.

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
        """
        Function display each element from list in Panel.

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
        """
        Function display Header and list of element.
        user selevt a element in list and his index is returned.

        Args:
            section (str): Hearder information. Section.

            list_element (list): List of element to display

        Returns:
            int: Index of element selected.
        """
        self.display_element_list(
            section=section, department=department, current_user_name=current_user_name, list_element=list_element
        )
        range_list = len(list_element)
        while True:
            result = IntPrompt.ask(
                f" Enter a number between [b]1[/b] and [b]{range_list}[/b]",
            )
            if result >= 1 and result <= range_list:
                break
            print(":pile_of_poo: [prompt.invalid]Number must be between 1 and range_list")
        return result - 1

    def get_address_info(self):
        pass
