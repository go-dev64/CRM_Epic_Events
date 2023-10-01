from crm.models.customer import Customer
from crm.models.element_administratif import Event
from crm.view.generic_view import GenericView
from rich.table import Table
from rich.prompt import Confirm


class SellerView:
    def __init__(self) -> None:
        self.generic_view = GenericView()

    def get_info_customer_view(
        self, department: str, current_user_name: str, section: str = "Create New Customer/Get Information"
    ) -> dict:
        """
        Function used to get information customer.
        The seller of customer is current user.

        Args:
            department (str): Department of user connected to display in header.
            current_user_name (str): User connected name to display in header.
            section (str, optional): Section information to display in header.Defaults to:
            "Create New Customer/Get Information".

        Returns:
            dict: Dictionnary with Customer information : {
                "name: str,"email_address":str,"phone_number":str,"company" : str
                }
        """
        customer_info = {}
        restrictions = [
            x for x in Customer().availables_attribue_list() if x.get("attribute_name") not in ["seller_contact"]
        ]
        self.generic_view.header(department=department, current_user=current_user_name, section=section)
        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            customer_info[attribute_name] = self.generic_view.string_form(restriction=restriction)
        return customer_info

    def get_event_info_view(
        self, department: str, current_user_name: str, section: str = "Create New Event/Get Information"
    ) -> dict:
        """Function used to get information Event.

        Args:
            department (str): Department of user connected to display in header.
            current_user_name (str): User connected name to display in header.
            section (str, optional): Section information to display in header.Defaults to:
            "Create New Event/Get Information".

        Returns:
            dict: Dictionnary with Event information :
             "name": int,"date_start": datetime,"date_end": datetime,"attendees": int, "note": str}
        """
        event_info = {}
        restrictions = [
            x
            for x in Event().availables_attribue_list()
            if x.get("attribute_name") not in ["supporter", "contract", "address"]
        ]
        self.generic_view.header(department=department, current_user=current_user_name, section=section)
        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            if restriction["parametre"]["type"] == str:
                event_info[attribute_name] = self.generic_view.string_form(restriction=restriction)
            elif restriction["parametre"]["type"] == int:
                event_info[attribute_name] = self.generic_view.integer_form(restriction=restriction)
            elif restriction["parametre"]["type"] == "datetime":
                if restriction["attribute_name"] == "date_start":
                    msg = "start"
                else:
                    msg = "end"
                event_info[attribute_name] = self.generic_view.date_form(msg=msg)

        return event_info
