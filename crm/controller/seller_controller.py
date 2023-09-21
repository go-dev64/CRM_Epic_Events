from crm.models.authentication import Authentication
from crm.view.customer_view import CustomerView
from crm.view.event_view import EventView
from crm.view.generic_view import GenericView


class SellerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.customer_view = CustomerView()
        self.event_view = EventView()

    @auth.is_authenticated
    def create_new_element(self, session):
        """
        Function redirect to create_new_customer or create_new_event functions according to user's choice.

        Args:
            session (_type_): _description_

        Returns:
            _type_: create_new_customer() or create_new_event()
        """
        while True:
            choice = self.generic_view.select_element_view()
            match choice:
                case 1:
                    return self.create_new_customer(session=session)
                case 2:
                    return self.create_new_event(session=session)
                case 3:
                    break

    @auth.is_authenticated
    def create_new_customer(self, session):
        """
        Function will create a new customer with the information entered by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: a new instance of Customer class.
        """
        customer_info = self.customer_view.get_info_customer()
        new_customer = session.current_user.create_new_customer(session=session, customer_info=customer_info)
        return new_customer

    @auth.is_authenticated
    def create_new_event(self, session):
        """
        Function will create a new event with the information entered by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: a new instance of Event class.
        """

        event_info = self.event_view.get_event_info()
        new_event = session.current_user.create_new_event(session=session, event_info=event_info)
        return new_event

    @auth.is_authenticated
    def select_customer_type_to_display(self, session):
        choice_list = ["Select all customers", "Select yours customers"]
        choice = self.generic_view.select_element_view(list_element=choice_list)
        match choice:
            case 0:
                customer_list = session.current_user.get_all_customers(session=session)
                element_selected = self.generic_view.display_element_list(list_element=customer_list)
                self.generic_view.display_element(element=element_selected)
            case 1:
                yours_customers_list = session.current_user.get_all_clients_of_user(session)
                element_selected = self.generic_view.display_element_list(list_element=yours_customers_list)
                self.generic_view.display_element(element=element_selected)

    @auth.is_authenticated
    def select_unpayed_contract(self, session):
        unpayed_contract_list = session.current_user
