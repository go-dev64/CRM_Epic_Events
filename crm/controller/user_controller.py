from crm.models.authentication import Authentication
from crm.models.users import User
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

        Returns:
            _type_: function choosen.
        """
        while True:
            element_list = [
                "Create element(like Customer, Contract...)",
                "Display element (like Customer, Contract, Event...)",
                "Update element",
                "Delete element",
                "Disconnection",
            ]
            choice = self.generic_view.select_element_view(
                section="Home Page",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=element_list,
            )
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
        """
        Function redirect to create function of user's departement.

        Returns:
            _type_: User's function to creating.
        """
        user_type = session.current_user_department
        match user_type:
            case "Manager":
                return self.manager_controller.create_new_element(session=session)
            case "Seller":
                return self.seller_controller.create_new_element(session=session)
            case "Supporter":
                return self.utils.create_new_address(session=session)

    @auth.is_authenticated
    def user_choice_is_reading(self, session):
        """
        According to current user' s choice, redirect to chosen action.

        Returns:
            _type_: _description_
        """
        element_list = [
            "Display Customers list ",
            "Display Contracts List",
            "Display Events list",
            "Back to previous menu",
        ]
        while True:
            choice = self.generic_view.select_element_view(
                section="Consultation Page / Choice",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=element_list,
            )
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
        """
        Function redirect to updating function of user's department.

        Returns:
            _type_: Updating function.
        """
        user_type = session.current_user_department
        match user_type:
            case "Manager":
                return self.manager_controller.update_element(session=session)
            case "Seller":
                return self.seller_controller.select_element_type_to_be_updated(session=session)
            case "Supporter":
                return self.supporter_controller.update_element(session=session)

    @auth.is_authenticated
    def user_choice_is_deleting(self, session):
        user_type = session.current_user_department
        match user_type:
            case "Manager":
                return self.manager_controller.delete_collaborator(session=session)
            case "Seller":
                return None
            case "Supporter":
                return None

    @auth.is_authenticated
    def get_customer_list(self, session):
        user_type = session.current_user_department
        if user_type != "Seller":
            customer_list = User().get_all_customers(session=session)
            return self.generic_view.display_element(customer_list)
        else:
            return self.seller_controller.select_customer_type_to_display(session=session)

    @auth.is_authenticated
    def get_contract_list(self, session):
        user_type = session.current_user_department
        if user_type != "Seller":
            contract_list = User().get_all_contracts(session=session)
            return self.generic_view.display_element(contract_list)
        else:
            return self.seller_controller.select_contract_type_to_display(session=session)

    @auth.is_authenticated
    def get_events_list(self, session):
        user_type = session.current_user_department
        if user_type == "Seller":
            event_list = User().get_all_events(session=session)
            return self.generic_view.display_element(event_list)
        elif user_type == "Manager":
            return self.manager_controller.display_event(session=session)
        else:
            return self.supporter_controller.display_event_of_user(session=session)
