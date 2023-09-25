from rich.console import Console
from rich import print
from rich.panel import Panel


class GenericView:
    def __init__(self) -> None:
        self.console = Console()

    def header(self, section):
        print("\033c", end="")  # Efface la page précédente
        title_panel = Panel(section, title="[i bold]CRM Epic Event[/i bold]")
        self.console.print(title_panel)

    def home_view(self):
        pass

    def display_element_list(self, list_element):
        for i in range(len(list_element)):
            print(f"{i} - {list_element[i]}")

    def display_element(self, list_element):
        element = self.select_element_view(list_element)
        print(element)
        return element

    def select_element_view(self, list_element):
        self.display_element_list(list_element=list_element)
        element_chosen = input
        return element_chosen

    def get_address_info(self):
        pass
