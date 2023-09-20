from crm.models.authentication import Authentication
from crm.view.customer_view import CustomerView
from crm.view.generic_view import GenericView


class SellerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.customer_view = CustomerView()

    @auth.is_authenticated
    def create_new_element(self, session):
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
        customer_info = self.customer_view.get_info_customer()
        new_customer = session.current_user.create_new_customer(session=session, customer_info=customer_info)
        return new_customer

    @auth.is_authenticated
    def create_new_event(self, session):
        print("get info customer")
        event_info = "input"
        new_customer = session.current_user.create_new_event(session=session, event_info=event_info)
        return new_customer
