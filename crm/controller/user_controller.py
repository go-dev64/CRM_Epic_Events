from crm.models.authentication import Authentication
from crm.models.utils import Utils
from crm.controller.manager_controller import ManagerController
from crm.controller.seller_controller import SellerController
from crm.controller.supporter_controller import SupporterController
from crm.view.generic_view import GenericView

# from crm.controller.supporter_controller import SupporterController


class UserController:
    auth = Authentication()

    def __init__(self) -> None:
        self.manager_controller = ManagerController()
        self.seller_controller = SellerController()
        self.supporter_controller = SupporterController()
        self.generic_view = GenericView()
        self.utils = Utils()

    @auth.is_authenticated
    def home_page(self, session):
        """
        Function redirect to Create element,Read element,
        Update element or Delete element according to the user's choice.

        Args:
            session (_type_): _description_

        Returns:
            _type_: function choosen.
        """
        while True:
            choice = self.generic_view.select_element_view()
            match choice:
                case 0:
                    return self.user_choice_is_creating(session=session)
                case 1:
                    return self.user_choice_is_reading(session=session)
                case 2:
                    return self.user_choice_is_updating(session=session)
                case 3:
                    return self.user_choice_is_deleting(session=session)
                case 4:
                    break

    @auth.is_authenticated
    def user_choice_is_creating(self, session):
        user_type = self.utils.get_type_of_user(session.current_user)
        match user_type:
            case "Manager":
                return self.manager_controller.create_new_element(session=session)
            case "Seller":
                return self.seller_controller.create_new_element(session=session)
            case "Supporter":
                return self.utils.create_new_address(session=session)

    @auth.is_authenticated
    def user_choice_is_reading(self, session):
        while True:
            choice = self.generic_view.select_element_view()
            match choice:
                case 0:
                    return self.get_customer_list(session=session)
                case 1:
                    return self.get_contract_list(session=session)
                case 2:
                    return self.get_events_list(session=session)
                case 3:
                    break

    @auth.is_authenticated
    def user_choice_is_updating(self, session):
        pass

    @auth.is_authenticated
    def user_choice_is_deleting(self, session):
        pass

    @auth.is_authenticated
    def get_customer_list(self, session):
        user_type = self.utils.get_type_of_user(session.current_user)
        if user_type != "Seller":
            customer_list = session.current_user.get_all_customers(session=session)
            return self.generic_view.display_element(customer_list)
        else:
            return self.seller_controller.select_customer_type_to_display(session=session)

    @auth.is_authenticated
    def get_contract_list(self, session):
        user_type = self.utils.get_type_of_user(session.current_user)
        if user_type != "Seller":
            contract_list = session.current_user.get_all_contracts(session=session)
            return self.generic_view.display_element(contract_list)
        else:
            return self.seller_controller.select_contract_type_to_display(session=session)

    @auth.is_authenticated
    def get_events_list(self, session):
        user_type = self.utils.get_type_of_user(session.current_user)
        if user_type != "Supporter":
            event_list = session.current_user.get_all_events(session=session)
            return self.generic_view.display_element(event_list)
        else:
            return self.supporter_controller.display_event_of_user(session=session)
