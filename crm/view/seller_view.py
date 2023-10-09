from crm.models.customer import Customer
from crm.models.element_administratif import Event
from crm.models.exceptions import EmailUniqueError
from crm.models.utils import Utils
from crm.view.generic_view import GenericView

from crm.view.login_view import LoginView


class SellerView:
    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.login_view = LoginView()
        self.utils = Utils()

    def get_customer_email(self, session) -> str:
        """The function is used to get a nomalize email and check if email is unique.

        Args:
            session (_type_): session sqlalchemy

        Raises:
            EmailUniqueError: Exception of unique email.

        Returns:
            str: normalize email.
        """
        while True:
            try:
                email = self.login_view.get_email()
                if not self.utils.check_customer_email_is_unique(session=session, email=email):
                    raise EmailUniqueError()
            except EmailUniqueError as msg:
                self.generic_view.console.print(msg)
            else:
                break

        return email

    def get_info_customer_view(self, session) -> dict:
        """
        Function used to get information customer.
        The seller of customer is current user.

        Args:
            session(): session sqlalchemy

        Returns:
            dict: Dictionnary with Customer information : {
                "name: str,"email_address":str,"phone_number":str,"company" : str
                }
        """
        section = "Create New Customer/Get Information"
        customer_info = {}
        restrictions = [
            x for x in Customer().availables_attribue_list() if x.get("attribute_name") not in ["seller_contact"]
        ]
        self.generic_view.header(
            department=session.current_user_department, current_user=session.current_user.name, section=section
        )
        for restriction in restrictions:
            attribute_name = restriction["attribute_name"]
            if attribute_name == "email_address":
                customer_info["email_address"] = self.get_customer_email(session=session)
            else:
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
                self.generic_view.console.print(f"Please, enter number of {attribute_name}")
                event_info[attribute_name] = self.generic_view.integer_form(restriction=restriction)
            elif restriction["parametre"]["type"] == "date":
                if restriction["attribute_name"] == "date_start":
                    msg = "start"
                else:
                    msg = "end"
                event_info[attribute_name] = self.generic_view.date_form(msg=msg)

        return event_info
