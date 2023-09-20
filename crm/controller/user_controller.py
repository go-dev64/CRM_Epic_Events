from crm.models.authentication import Authentication
from crm.controller.manager_controller import ManagerController
from crm.controller.seller_controller import SellerController
from crm.view.user_view import UserView

# from crm.controller.supporter_controller import SupporterController


class UserController:
    auth = Authentication()

    def __init__(self) -> None:
        self.manager_controller = ManagerController()
        self.seller_controller = SellerController()
        # self.supporter_controller = SupporterController()
        self.user_view = UserView()

    @auth.is_authenticated
    def home_page(self, session):
        while True:
            choice = self.user_view.view_select_choice()
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
        user_type = type(session.current_user).__name__
        match user_type:
            case "Manager":
                return self.manager_controller.create_new_user(session=session)
            case "Seller":
                return self.seller_controller.create(session=session)
            case "Supporter":
                return self.supporter_controller.create(session=session)

    @auth.is_authenticated
    def user_choice_is_updating(self, session):
        pass

    @auth.is_authenticated
    def user_choice_is_reading(self, session):
        pass

    @auth.is_authenticated
    def user_choice_is_deleting(self, session):
        pass

    @auth.is_authenticated
    def get_customer_list(self, session):
        customer_list = session.current_user.get_all_customers(session=session)
        print(customer_list)

    @auth.is_authenticated
    def get_contract_list(self, session):
        contract_list = session.current_user.get_all_contracts(session=session)
        print(contract_list)

    @auth.is_authenticated
    def get_events_list(self, session):
        event_list = session.current_user.get_all_events(session=session)
        print(event_list)
