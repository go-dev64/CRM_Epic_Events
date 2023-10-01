from crm.models.authentication import Authentication
from crm.models.customer import Customer
from crm.models.element_administratif import Contract, Event
from crm.models.users import Manager, Supporter, User
from crm.models.utils import Utils
from crm.view.generic_view import GenericView
from crm.view.manager_view import ManagerView
from crm.view.user_view import UserView


class ManagerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.user_view = UserView()
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
            choice = self.generic_view.select_element_in_menu_view(
                section="Create new element",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=choice_list,
            )
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
    def create_new_user(self, session) -> User:
        """Function of new user's cretaion.
        According to user's choice, the function willto create a new manager, or new seller or new supporter.

        Returns:
            User: A new instance of Manager class , or Seller class or Supporter class.
        """
        while True:
            department_list = ["Manager", "Seller", "Supporter", "Back to previous menu"]
            user_info = self.user_view.get_user_info_view(
                section="Create new collaborator",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
            )
            department = self.generic_view.select_element_in_menu_view(department_list)
            match department:
                case 0:
                    new_user = Manager().create_new_manager(session=session, user_info=user_info)
                    return new_user
                case 1:
                    new_user = Manager().create_new_seller(session=session, user_info=user_info)
                    return new_user
                case 2:
                    new_user = Manager().create_new_supporter(session=session, user_info=user_info)
                    return new_user
                case 3:
                    break

    @auth.is_authenticated
    def get_info_contract(self, session) -> dict:
        """Function is used to get a contract info by user.
        {"total_amount: int,
        "remaining":int,
        "signedècontract":bool,
        "customer: Instance of Customer Class
        }

        Args:
            session (_type_): Sqalachemay actual session.

        Returns:
            dict: {"total_amount: int, "remaining":int,"signed_contract":bool,"customer: Instance of Customer}
        """
        contract_info = self.manager_view.get_info_contract_view(
            department=session.current_user_department, current_user_name=session.current_user.name
        )
        contract_info["customer"] = self.select_customer_of_contract(session=session)
        return contract_info

    @auth.is_authenticated
    def select_customer_of_contract(self, session) -> Customer:
        """The function is used to select a customer in customers list.

        Args:
            session (_type_): actual Sqlalchemy session.

        Returns:
            Customer: Customer selected by user.
        """
        customers_list = Manager().get_all_customers(session=session)
        choice = self.generic_view.select_element_in_menu_view(
            section="Select Customer of contract",
            department=session.current_user_department,
            current_user_name=session.current_user.name,
            list_element=customers_list,
        )
        return customers_list[choice]

    @auth.is_authenticated
    def create_new_contract(self, session) -> Contract:
        """New contract create function.

        Args:
            session (_type_): actual sqlalchemy session.

        Returns:
            Contract: new contract created.
        """
        contract_info = self.get_info_contract(session=session)
        new_contract = Manager().create_new_contract(session=session, contract_info=contract_info)
        return new_contract

    @auth.is_authenticated
    def display_event(self, session):
        """Function enabling the user to select an action between display all events,
        all events without supporter , and back.

        Returns:
            _type_: Return the function executing the action chosen by user.
        """
        choice_list = ["Display all Events", "Display all Events without Supporter", "Back to previous menu"]
        attributes_displayed = Event().availables_attribue_list()
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Display Events/ Select an action",
                department=session.current_user_department,
                current_user_name=session.current_user,
                list_element=choice_list,
            )
            match choice:
                case 0:
                    events_list = Manager().get_all_events(session=session)
                    return self.generic_view.display_elements(
                        session=session,
                        section="Display Events",
                        title_table="All Event",
                        elements_list=events_list,
                        attributes=attributes_displayed,
                    )
                case 1:
                    events_without_support_list = Manager().get_all_event_without_support(session=session)
                    return self.generic_view.display_elements(
                        session=session,
                        section="Display Events",
                        title_table="Event without Supporter",
                        elements_list=events_without_support_list,
                        attributes=attributes_displayed,
                    )
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
            element = self.generic_view.select_element_in_menu_view(list_of_choice)
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

    def select_new_department(self, session, section, collaborator):
        """Function is used to select the new department, in list, for the selected collaborator.

        Args:
            session (_type_): session sqlalchemy
            section (str): Section information to be displayed in header
            collaborator (_type_): collaborator selected

        Returns:
            _type_: _description_
        """
        department_list = self._get_department_list(collaborator=collaborator)
        user_choice = self.generic_view.select_element_in_menu_view(
            section=section,
            department=session.current_user_department,
            current_user_name=session.current_user.name,
            list_element=department_list,
        )
        return department_list[user_choice]

    @auth.is_authenticated
    def select_collaborator(self, session) -> User:
        """The function is used to select a collaborator.

        Returns:
            User: collaborator selected.
        """
        collaborator_list = Manager().get_all_users(session=session)
        collaborator_selected = self.utils._select_element_in_list(
            session=session, section="Update Collaborator/Select Collaborator", element_list=collaborator_list
        )
        return collaborator_selected

    @auth.is_authenticated
    def change_collaborator_department(self, session, collaborator_selected: User):
        """The function is used to change department of collaborator selected.
        User select a new department for a collaborator selected.

        Args:
            session (): _description_
            collaborator_selected (User): Collbaorator to be udpated.

        Returns:
            _type_: Collaborator Updated.
        """
        new_department = self.select_new_department(
            session=session,
            section="Update Collaborator/Select new department",
            collaborator=collaborator_selected,
        )
        return Manager().change_user_department(
            session=session, collaborator=collaborator_selected, new_department=new_department
        )

    def change_collaborator_attribute(self, session, collaborator_selected: User, attribute_selected: str):
        """The function is used to update an attribute of collaborator.
        After inut new value by user , the fucntion update attrubite.

        Args:
            session (_type_): sqlalchemy session.
            collaborator_selected (User): Collaborator to be updates.
            attribute_selected (str): attribute to be updated.

        Returns:
            _type_: User updated.
        """
        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=collaborator_selected,
            attribute_to_updated=attribute_selected,
        )
        return Manager().update_user(
            session=session,
            collaborator=collaborator_selected,
            update_attribute=attribute_selected,
            new_value=new_value,
        )

    @auth.is_authenticated
    def update_collaborator(self, session):
        """Function updates a collaborator.

        Returns:
            _type_: collaborator updated.
        """
        collaborator_selected = self.select_collaborator(session=session)
        attribute_selected = self.utils._select_attribut_of_element(
            session=session, section="Update Collaborator/Select Attribute to updated", element=collaborator_selected
        )
        if attribute_selected == "department":
            return self.change_collaborator_department(session=session, collaborator_selected=collaborator_selected)
        else:
            return self.change_collaborator_attribute(
                session=session, collaborator_selected=collaborator_selected, attribute_selected=attribute_selected
            )

    @auth.is_authenticated
    def select_contract(self, session) -> Contract:
        """The function is used to select a Contract.

        Returns:
            Contract: Contract selected.
        """
        contracts = Manager().get_all_contracts(session=session)
        contract_selected = self.utils._select_element_in_list(
            session=session, section="Update Contract/Select Contract", element_list=contracts
        )
        return contract_selected

    def change_customer_of_contract(self, session, contract_selected: Contract) -> Contract:
        """the function is used to change customer of contract, after selected a new customer by user.

        Args:
            session (_type_): _description_
            contract_selected (Contract): Contract to be updated.

        Returns:
            Contract: Contract updated.
        """
        new_customer = self.select_customer_of_contract(session=session)
        return Manager().update_contract(
            session=session, contract=contract_selected, attribute_update="customer", new_value=new_customer
        )

    @auth.is_authenticated
    def update_contract(self, session) -> Contract:
        """The function is used to update a contract.

        Args:
            session (_type_): _description_

        Returns:
            Contract: Contract updated.
        """
        contract = self.select_contract(session=session)
        attribute_selected = self.utils._select_attribut_of_element(
            session=session, section=" Update Contract/Select Attribute to updated", element=contract
        )
        if attribute_selected == "customer":
            return self.change_customer_of_contract(session=session, contract_selected=contract)
        else:
            new_value = self.generic_view.get_new_value_of_attribute(
                section=f"New Value of {attribute_selected}",
                department=session.current_user_department,
                current_user=session.current_user.name,
                element=contract,
                attribute_selected=attribute_selected,
            )
            Manager().update_contract(
                session=session, contract=contract, attribute_update=attribute_selected, new_value=new_value
            )

    @auth.is_authenticated
    def select_supporter(self, session) -> Supporter:
        """The function is used to select a suporter for event.

        Args:
            session (_type_): _description_

        Returns:
            Supporter: Supporter selected
        """
        supporters = Manager().get_all_supporter(session=session)
        supporter = self.utils._select_element_in_list(
            session=session, section="Update Event/ Select new Supporter", element_list=supporters
        )
        return supporter

    @auth.is_authenticated
    def update_event(self, session):
        """The function change supporter of Event.

        Args:
            session (_type_): _description_
        """
        events = Manager().get_all_events(session=session)
        event = self.utils._select_element_in_list(session=session, section="Update/Select Event", element_list=events)
        supporter = self.select_supporter(session=session)
        Manager().change_supporter_of_event(session=session, event=event, new_supporter=supporter)

    @auth.is_authenticated
    def delete_collaborator(self, session):
        collaborator_list = Manager().get_all_users(session=session)
        collaborator_list.remove(session.current_user)
        collaborator_selected = self.utils._select_element_in_list(element_list=collaborator_list)
        Manager().delete_collaborator(session=session, collaborator_has_delete=collaborator_selected)
