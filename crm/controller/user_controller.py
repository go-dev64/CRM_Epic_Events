from crm.models.authentication import Authentication
from crm.models.customer import Customer
from crm.models.element_administratif import Address, Contract, Event
from crm.models.users import Supporter, User
from crm.models.utils import Utils
from crm.controller.manager_controller import ManagerController
from crm.controller.seller_controller import SellerController
from crm.controller.supporter_controller import SupporterController
from crm.view.generic_view import GenericView


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
            choice = self.generic_view.select_element_in_menu_view(
                section="Home Page",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=element_list,
            )
            match choice:
                case 0:
                    self.user_choice_is_creating(session=session)
                case 1:
                    self.user_choice_is_reading(session=session)
                case 2:
                    self.user_choice_is_updating(session=session)
                case 3:
                    self.user_choice_is_deleting(session=session)
                case 4:
                    break

    @auth.is_authenticated
    def user_choice_is_creating(self, session):
        """
        Function redirect to create function of user's departement.

        Returns:
            _type_: User's function to creating.
        """
        match session.current_user_department:
            case "Manager":
                self.manager_controller.create_new_element(session=session)
            case "Seller":
                self.seller_controller.create_new_element(session=session)
            case "Supporter":
                self.utils.create_new_address(session=session)

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
            "Display Address",
            "Back to previous menu",
        ]
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Consultation Page / Choice",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=element_list,
            )
            match choice:
                case 0:
                    self.get_customer_list(session=session)
                case 1:
                    self.get_contract_list(session=session)
                case 2:
                    self.get_events_list(session=session)
                case 3:
                    self.get_address_list(session=session)
                case 4:
                    break

    @auth.is_authenticated
    def user_choice_is_updating(self, session):
        """Function redirect to updating function of user's department.

        Returns:
            _type_: Updating function.
        """
        match session.current_user_department:
            case "Manager":
                self.manager_controller.update_element(session=session)
            case "Seller":
                self.seller_controller.select_element_type_to_be_updated(session=session)
            case "Supporter":
                self.supporter_controller.update_element(session=session)

    @auth.is_authenticated
    def user_choice_is_deleting(self, session):
        """Function redirect to the delete function of user's department.

        Args:
            session (_type_): actual session.

        Returns:
            _type_: Delete function of department.
        """

        match session.current_user_department:
            case "Manager":
                self.manager_controller.delete_collaborator(session=session)
            case "Seller":
                self.generic_view.forbidden_acces(session=session, section="Delele view/ Forbidden Acces")
            case "Supporter":
                self.generic_view.forbidden_acces(session=session, section="Delele view/ Forbidden Acces")

    @auth.is_authenticated
    def get_customer_list(self, session):
        """Function redirect to the display customer functions of user's department.
        if len(list) < 0: no data message to displyed.

        Args:
            session (_type_): _description_

        Returns:
            _type_: display customer functions of department.
        """

        if session.current_user_department == "Seller":
            self.seller_controller.select_customer_type_to_display(session=session)

        else:
            self.seller_controller.display_all_customers(session=session)

    @auth.is_authenticated
    def get_contract_list(self, session):
        """Function redirect to the display contracts functions of user's department.
        if len(list) < 0: no data message to displyed.
        Args:
            session (_type_): _description_

        Returns:
            _type_: display custocontractsmer functions of department.
        """

        if session.current_user_department == "Seller":
            self.seller_controller.select_contract_type_to_display(session=session)
        else:
            contract_list = User().get_all_contracts(session=session)
            if len(contract_list) > 0:
                self.generic_view.display_elements(
                    session=session,
                    section="Display Contracts",
                    title_table="All Contracts",
                    elements_list=contract_list,
                )
            else:
                self.generic_view.no_data_message(
                    session=session, section="Display all Contract", msg="for this section"
                )

    @auth.is_authenticated
    def get_events_list(self, session):
        """Function redirect to the display events functions of user's department.
        if len(list) < 0: no data message to displyed.
        Args:
            session (_type_): _description_

        Returns:
            _type_: display events functions of department.
        """

        if session.current_user_department == "Supporter":
            self.supporter_controller.display_event(session=session)

        elif session.current_user_department == "Manager":
            self.manager_controller.display_event(session=session)
        else:
            event_list = User().get_all_events(session=session)
            if len(event_list) > 0:
                self.generic_view.display_elements(
                    session=session,
                    section="Display Events",
                    title_table="All Event",
                    elements_list=event_list,
                )
            else:
                self.generic_view.no_data_message(
                    session=session, section="Display all Events", msg="for this section"
                )

    @auth.is_authenticated
    def get_address_list(self, session):
        """Function display list of address.

        Returns:
            _type_: display address list.
        """
        address_list = User().get_all_adress(session=session)
        if len(address_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section="Display Address",
                title_table="All Address",
                elements_list=address_list,
            )
        else:
            self.generic_view.no_data_message(session=session, section="Display all Address", msg="for this section")
