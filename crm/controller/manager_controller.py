from crm.models.authentication import Authentication
from crm.models.element_administratif import Event
from crm.models.utils import Utils
from crm.view.contract_view import ContractView
from crm.view.generic_view import GenericView
from crm.view.manager_view import ManagerView
from crm.view.user_view import UserView


class ManagerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.user_view = UserView()
        self.contract_view = ContractView()
        self.manager_view = ManagerView()
        self.utils = Utils()

    @auth.is_authenticated
    def create_new_element(self, session):
        """
        Function redirects to create a new user or a new contract according to the user's choice.

        Returns:
            _type_: create_new_user or create_new_contract functions.
        """
        while True:
            choice_list = [
                "Create new Collaborator",
                "Create new contract",
                "Create new address",
                "Back to previous menu",
            ]
            choice = self.generic_view.select_element_view(choice_list)
            match choice:
                case 0:
                    return self.create_new_user(session=session)
                case 1:
                    return self.create_new_contract(session=session)
                case 2:
                    return self.utils.create_new_address(session=session)
                case 3:
                    break

    @auth.is_authenticated
    def create_new_user(self, session):
        """
        Function of new user's cretaion.
        According to user's choice, the function willto create a new manager, or new seller or new supporter.

        Returns:
            _type_: A neww instance of Manager class , or Seller class or Supporter class.
        """
        while True:
            department_list = ["Manager", "Seller", "Supporter", "Back to previous menu"]
            user_info = self.user_view.get_user_info_view()
            department = self.generic_view.select_element_view(department_list)
            match department:
                case 0:
                    new_user = session.current_user.create_new_manager(session=session, user_info=user_info)
                    return new_user
                case 1:
                    new_user = session.current_user.create_new_seller(session=session, user_info=user_info)
                    return new_user
                case 2:
                    new_user = session.current_user.create_new_supporter(session=session, user_info=user_info)
                    return new_user
                case 3:
                    break

    @auth.is_authenticated
    def create_new_contract(self, session):
        """
        New contract creation function.

        Returns:
            _type_: new instance of Contract class.
        """
        contract_info = self.contract_view.get_info_contract()
        new_contract = session.current_user.create_new_contract(session=session, contract_info=contract_info)
        return new_contract

    @auth.is_authenticated
    def select_event_to_display(self, session) -> Event:
        """
        Function display a element selecting by current user from list of all events.

        Returns:
            Event: Instance of Events.
        """
        events_list = session.current_user.get_all_events(session=session)
        return self.generic_view.display_element(events_list)

    @auth.is_authenticated
    def select_event_without_supporter_to_display(self, session) -> Event:
        """
        Function display a element selecting by current user,
        from list of all events without support department contact.

        Returns:
            Event: Instance of Events.
        """
        event_list = session.current_user.get_all_event_without_support(session=session)
        return self.generic_view.display_element(event_list)

    @auth.is_authenticated
    def display_event(self, session):
        """
        Function enabling the user to select an action between display all events,
        all events without supporter , and back.

        Returns:
            _type_: Return the function executing the action chosen by user.
        """
        while True:
            choice_list = ["Display all Events", "Display all Events without Supporter", "Back to previous menu"]
            choice = self.generic_view.select_element_view(choice_list)
            match choice:
                case 0:
                    return self.select_event_to_display(session=session)
                case 1:
                    return self.select_event_without_supporter_to_display(session=session)
                case 2:
                    break

    @auth.is_authenticated
    def update_element(self, session):
        """
        Function enabling the user to select an action between:
        "Update Collaborator",
        "Update Contract",
        "Update Event",
        "Update Address",
        "back to previous menu".

        Returns:
            _type_: Return the function executing the action chosen by user.
        """
        list_of_choice = [
            "Update Collaborator",
            "Update Contract",
            "Update Event",
            "Update Address",
            "Back to previous menu",
        ]
        while True:
            element = self.generic_view.select_element_view(list_of_choice)
            match element:
                case 0:
                    return self.update_collaborator(session=session)
                case 1:
                    return self.update_contract(session=session)
                case 2:
                    return self.update_event(session=session)
                case 3:
                    return self.utils.update_address(session=session)
                case 4:
                    break

    def _get_department_list(self, collaborator):
        """
        Function defines the departments available for a user to change department.

        Returns:
            _type_: available department list.
        """
        department_list = ["Manager", "Seller", "Supporter"]
        user_type = self.utils.get_type_of_user(collaborator)
        department_list.remove(user_type)
        return department_list

    def _select_new_department(self, collaborator):
        """
        Function used to select the new department, in list, for the selected employee.

        Returns:
            _type_: new department
        """
        department_list = self._get_department_list(collaborator=collaborator)
        user_choice = self.generic_view.select_element_view(department_list)
        return department_list[user_choice]

    @auth.is_authenticated
    def update_collaborator(self, session):
        """
        Function updates a collaborator.

        Returns:
            _type_: collaborator updated.
        """
        collaborator_list = session.current_user.get_all_users(session=session)
        collaborator_selected = self.utils._select_element_in_list(element_list=collaborator_list)
        attribute_selected = self.utils._select_attribut_of_element(element=collaborator_selected)
        if attribute_selected == "department":
            new_department = self._select_new_department(collaborator_selected)
            return session.current_user.change_user_department(
                session=session, collaborator=collaborator_selected, new_department=new_department
            )
        else:
            new_value = self.utils._get_new_value_of_attribut(
                element=collaborator_selected, attribute_to_updated=attribute_selected
            )
            return session.current_user.update_user(
                session=session,
                collaborator=collaborator_selected,
                update_attribute=attribute_selected,
                new_value=new_value,
            )

    @auth.is_authenticated
    def update_contract(self, session):
        contracts = session.current_user.get_all_contracts(session=session)
        contract = self.utils._select_element_in_list(element_list=contracts)
        attribute_selected = self.utils._select_attribut_of_element(element=contract)
        if attribute_selected == "customer":
            customer_list = session.current_user.get_all_customers(session=session)
            new_customer = self.utils._select_element_in_list(element_list=customer_list)
            session.current_user.update_contract(
                session=session, contract=contract, attribute_update=attribute_selected, new_value=new_customer
            )
        else:
            new_value = self.utils._get_new_value_of_attribut(
                element=contract, attribute_to_updated=attribute_selected
            )
            session.current_user.update_contract(
                session=session, contract=contract, attribute_update=attribute_selected, new_value=new_value
            )

    def _select_supporter(self, session):
        """
        Function select a supporter in list.
        """
        supporters = session.current_user.get_all_supporter(session=session)
        supporter = self.utils._select_element_in_list(element_list=supporters)
        return supporter

    @auth.is_authenticated
    def update_event(self, session):
        """
        Function change or add a supporter to event.

        """
        events = session.current_user.get_all_events(session=session)
        event = self.utils._select_element_in_list(element_list=events)
        supporter = self._select_supporter(session=session)
        session.current_user.change_supporter_of_event(session=session, event=event, new_supporter=supporter)
