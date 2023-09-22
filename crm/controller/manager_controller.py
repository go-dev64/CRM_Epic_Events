from crm.models.authentication import Authentication
from crm.models.element_administratif import Event
from crm.models.utils import Utils
from crm.view.contract_view import ContractView
from crm.view.generic_view import GenericView
from crm.view.user_view import UserView


class ManagerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.user_view = UserView()
        self.contract_view = ContractView()
        self.utils = Utils()

    @auth.is_authenticated
    def create_new_element(self, session):
        """
        Function redirects to create a new user or a new contract according to the user's choice.

        Args:
            session (_type_): _description_

        Returns:
            _type_: create_new_user or create_new_contract functions.
        """
        while True:
            choice = self.generic_view.select_element_view()
            match choice:
                case 1:
                    return self.create_new_user(session=session)
                case 2:
                    return self.create_new_contract(session=session)
                case 3:
                    return self.utils.create_new_address(session=session)
                case 4:
                    break

    @auth.is_authenticated
    def create_new_user(self, session):
        """
        Function of new user's cretaion.
        According to user's choice, the function willto create a new manager, or new seller or new supporter.

        Args:
            session (_type_): _description_

        Returns:
            _type_: A neww instance of Manager class , or Seller class or Supporter class.
        """
        while True:
            user_info = self.user_view.get_user_info_view()
            department = self.generic_view.select_element_view()
            match department:
                case 1:
                    new_user = session.current_user.create_new_manager(session=session, user_info=user_info)
                    return new_user
                case 2:
                    new_user = session.current_user.create_new_seller(session=session, user_info=user_info)
                    return new_user
                case 3:
                    new_user = session.current_user.create_new_supporter(session=session, user_info=user_info)
                    return new_user
                case 4:
                    break

    @auth.is_authenticated
    def create_new_contract(self, session):
        """
        New contract creation function.

        Args:
            session (_type_): _description_

        Returns:
            _type_: new instance of Contract class.
        """
        contract_info = self.contract_view.get_info_contract()
        new_contract = session.current_user.create_new_contract(session=session, contract_info=contract_info)
        return new_contract

    @auth.is_authenticated
    def select_event_to_display(self, session) -> Event:
        events_list = session.current_user.get_all_events(session=session)
        return self.generic_view.display_element(events_list)

    @auth.is_authenticated
    def select_event_without_supporter_to_display(self, session):
        event_list = session.current_user.get_all_event_without_support(session=session)
        return self.generic_view.display_element(event_list)

    @auth.is_authenticated
    def display_event(self, session):
        while True:
            choice_list = ["Display all Events", "Display all Events without Supporter", "Back"]
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
        list_of_choice = [
            "Update Collaborator",
            "Update Contract",
            "Update Event",
            "Update Address",
            "back to previous menu",
        ]
        while True:
            element = self.generic_view.select_element_view()
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

    def _select_collaborator(self, session):
        collaborator_list = session.current_user.get_all_users(session=session)
        user_choice = self.generic_view.select_element_view(collaborator_list)
        return collaborator_list[user_choice]

    def _select_attribute_collaborator(self):
        updatable_attribute_list = ["name", "email_address", "phone_number", "password", "department"]
        user_choice = self.generic_view.select_element_view(updatable_attribute_list)
        return updatable_attribute_list[user_choice]

    def _get_department_list(self, collaborator):
        department_list = ["Manager", "Seller", "Supporter"]
        user_type = self.utils.get_type_of_user(collaborator)
        department_list = department_list.remove(user_type)
        return department_list

    def _select_new_department(self, collaborator):
        department_list = self._get_department_list(collaborator=collaborator)
        user_choice = self.generic_view.select_element_view(department_list)
        return department_list[user_choice]

    def _get_new_collaborator_attribute(self, old_attribute):
        attribute = {
            "name": [str, 50],
            "email_address": [str, 100],
            "phone_number": [str, 10],
            "password": [str, None],
        }
        restriction = attribute[old_attribute]
        new_value = self.manager_view.get_attribute(restriction=restriction)
        return new_value

    ### TO DO =Create manager_view.get_attribute(restriction=restriction) + test

    @auth.is_authenticated
    def update_collaborator(self, session):
        collaborator_selected = self._select_collaborator(session=session)
        attribute_selected = self._select_attribute_in_list()
        if attribute_selected == "department":
            new_department = self._select_new_department(collaborator_selected)
            return session.current_user.change_user_department(
                session=session, collaborator=collaborator_selected, new_department=new_department
            )
        else:
            new_value = self._get_attribute(old_attribute=attribute_selected)
            return session.current_user.update_user(
                session=session,
                collaborator=collaborator_selected,
                update_attribute=attribute_selected,
                new_value=new_value,
            )

    @auth.is_authenticated
    def update_contract(self):
        pass

    @auth.is_authenticated
    def update_event(self):
        pass
