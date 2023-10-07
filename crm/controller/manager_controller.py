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
                    self.create_new_user(session=session)
                case 1:
                    self.create_new_contract(session=session)
                case 2:
                    self.utils.create_new_address(session=session)
                case 3:
                    break

    @auth.is_authenticated
    def create_new_user(self, session) -> User:
        """Function of new user's cretaion.
        According to user's choice, the function willto create a new manager, or new seller or new supporter.

        Returns:
            User: A new instance of Manager class , or Seller class or Supporter class.
        """
        section = "Create new collaborator"
        department_list = ["Manager", "Seller", "Supporter"]
        user_info = self.user_view.get_user_info_view(section=section, session=session)
        department = self.generic_view.select_element_in_menu_view(
            section=section,
            department=session.current_user_department,
            current_user_name=session.current_user.name,
            list_element=department_list,
        )
        if self.generic_view.ask_comfirmation(message=section):
            match department:
                case 0:
                    new_collaborator = Manager().create_new_manager(session=session, user_info=user_info)
                    self.generic_view.confirmation_msg(section=section, session=session, msg="Operation succesfull!")
                    return new_collaborator
                case 1:
                    new_collaborator = Manager().create_new_seller(session=session, user_info=user_info)
                    self.generic_view.confirmation_msg(section=section, session=session, msg="Operation succesfull!")
                    return new_collaborator
                case 2:
                    new_collaborator = Manager().create_new_supporter(session=session, user_info=user_info)
                    self.generic_view.confirmation_msg(section=section, session=session, msg="Operation succesfull!")
                    return new_collaborator
        else:
            self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def get_info_contract(self, session) -> dict:
        """Function is used to get a contract info by user.

        Args:
            session (_type_): Sqalachemay actual session.

        Returns:
            dict: {"total_amount: int, "remaining":int,"signed_contract":bool,"customer: Instance of Customer}
        """
        contract_info = self.manager_view.get_info_contract_view(
            section="Create new Contract/ Contract Info",
            department=session.current_user_department,
            current_user_name=session.current_user.name,
        )
        contract_info["customer"] = self.select_customer_of_contract(session=session)
        return contract_info

    @auth.is_authenticated
    def select_customer_of_contract(self, session) -> Customer or None:
        """The function is used to select a customer in customers list.


        Args:
            session (_type_): actual Sqlalchemy session.

        Returns:
            Customer: Customer selected by user or None if customer list is empty.

        """
        customers_list = Manager().get_all_customers(session=session)
        if len(customers_list) > 0:
            choice = self.generic_view.select_element_in_menu_view(
                section="Select Customer of contract",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=customers_list,
            )
            return customers_list[choice]
        else:
            return None

    @auth.is_authenticated
    def create_new_contract(self, session) -> Contract:
        """New contract create function.

        Args:
            session (_type_): actual sqlalchemy session.

        Returns:
            Contract: new contract created.
        """
        section = "Create new Contract"
        contract_info = self.get_info_contract(session=session)
        if contract_info["customer"] != None:
            if self.generic_view.ask_comfirmation(message=section):
                new_contract = Manager().create_new_contract(session=session, contract_info=contract_info)
                self.generic_view.confirmation_msg(section=section, session=session, msg="Operation succesfull!")
                return new_contract
            else:
                self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")
        else:
            self.generic_view.no_data_message(
                session=session,
                section=section,
                msg="There are no availble customer. Create new Contract is not possible!",
            )

    @auth.is_authenticated
    def display_all_event(self, session):
        """The function is used for display all events.

        Args:
            session (_type_): _description_
        """
        event_list = Manager().get_all_events(session=session)
        if len(event_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section="Display Events",
                title_table="All Event",
                elements_list=event_list,
            )
        else:
            self.generic_view.no_data_message(
                session=session, section="Display all Events", msg="No data for All Event"
            )

    @auth.is_authenticated
    def display_all_event_without_supporter(self, session):
        """The function is used for display all events.

        Args:
            session (_type_): _description_
        """
        events_without_support_list = Manager().get_all_event_without_support(session=session)
        if len(events_without_support_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section="Display Events",
                title_table="Event without Supporter",
                elements_list=events_without_support_list,
            )
        else:
            self.generic_view.no_data_message(
                session=session, section="Display all Events", msg="No data for Event without Supporter"
            )

    @auth.is_authenticated
    def display_event(self, session):
        """Function enabling the user to select an action between display all events,
        all events without supporter , and back.

        Returns:
            _type_: Return the function executing the action chosen by user.
        """
        choice_list = ["Display all Events", "Display all Events without Supporter", "Back to previous menu"]
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Display Events/ Select an action",
                department=session.current_user_department,
                current_user_name=session.current_user,
                list_element=choice_list,
            )
            match choice:
                case 0:
                    self.display_all_event(session=session)
                case 1:
                    self.display_all_event_without_supporter(session=session)
                case 2:
                    break

    @auth.is_authenticated
    def update_element(self, session):
        """Function enabling the user to select an action between:
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
            element = self.generic_view.select_element_in_menu_view(
                section="Update/ Select element to Update",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=list_of_choice,
            )
            match element:
                case 0:
                    self.update_collaborator(session=session)
                case 1:
                    self.update_contract(session=session)
                case 2:
                    self.update_event(session=session)
                case 3:
                    self.utils.update_address(session=session)
                case 4:
                    break

    def _get_department_list(self, collaborator: User) -> list:
        """Function defines the departments available for a user to change department.

        Returns:
            list: available department list.
        """
        department_list = ["Manager", "Seller", "Supporter"]
        user_type = self.utils.get_type_of_user(collaborator)
        department_list.remove(user_type)
        return department_list

    def select_new_department(self, session, section, collaborator: User) -> str:
        """Function is used to select the new department, in list, for the selected collaborator.

        Args:
            session (_type_): session sqlalchemy
            section (str): Section information to be displayed in header
            collaborator (User): collaborator selected.

        Returns:
            str: new department of collaborator selected selected by user.
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
            User: collaborator selected or None if len list collaborator=0.
        """
        collaborator_list = Manager().get_all_users(session=session)
        if len(collaborator_list) > 0:
            collaborator_selected = self.utils._select_element_in_list(
                session=session, section="Update Collaborator/Select Collaborator", element_list=collaborator_list
            )
            return collaborator_selected
        else:
            return None

    @auth.is_authenticated
    def change_collaborator_department(self, session, collaborator_selected: User) -> User:
        """The function is used to change department of collaborator selected.
        User select a new department for a collaborator selected.

        Args:
            session (): _description_
            collaborator_selected (User): Collbaorator to be udpated.

        Returns:
            User: Collaborator Updated.
        """
        section = " Update Collaborator/Select new department"
        new_department = self.select_new_department(
            session=session,
            section=" Update Collaborator/Select new department",
            collaborator=collaborator_selected,
        )
        if self.generic_view.ask_comfirmation(message=section):
            Manager().change_user_department(
                session=session, collaborator=collaborator_selected, new_department=new_department
            )
            self.generic_view.confirmation_msg(
                session=session, section=" Update Collaborator", msg="Operation succesfull!"
            )
        else:
            self.generic_view.no_data_message(
                session=session, section=" Update Collaborator", msg="Operation Cancelled!"
            )

    @auth.is_authenticated
    def change_collaborator_attribute(self, session, collaborator_selected: User, attribute_selected: str) -> User:
        """The function is used to update an attribute of collaborator.
        After inut new value by user , the fucntion update attrubite.

        Args:
            session (_type_): sqlalchemy session.
            collaborator_selected (User): Collaborator to be updates.
            attribute_selected (str): attribute to be updated.

        Returns:
            User: User updated.
        """
        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=collaborator_selected,
            attribute_selected=attribute_selected,
        )
        if self.generic_view.ask_comfirmation(message="Upadte Callaborator"):
            Manager().update_user(
                collaborator=collaborator_selected,
                update_attribute=attribute_selected,
                new_value=new_value,
            )
            self.generic_view.confirmation_msg(
                session=session, section=" Update Collaborator", msg="Operation succesfull!"
            )
        else:
            self.generic_view.no_data_message(
                session=session, section=" Update Collaborator", msg="Operation Cancelled!"
            )

    @auth.is_authenticated
    def change_password(self, session, collaborator_selected: User) -> User:
        """The function is used to change password of collaborator selected.

        Args:
            session (_type_): _description_
            collaborator_selected (User):Collaborator selected.
        Returns:
            User: Collaborator with new password.
        """
        section = f"Update/Changing the {collaborator_selected} password"
        self.generic_view.header(
            section=section, department=session.current_user_department, current_user=session.current_user.name
        )
        password = self.user_view._get_user_password()
        if self.generic_view.ask_comfirmation(message="Upadte Callaborator"):
            Manager().update_user(
                collaborator=collaborator_selected,
                update_attribute="password",
                new_value=password,
            )
            self.generic_view.confirmation_msg(
                session=session, section=" Update Collaborator", msg="Operation succesfull!"
            )
        else:
            self.generic_view.no_data_message(
                session=session, section=" Update Collaborator", msg="Operation Cancelled!"
            )

    @auth.is_authenticated
    def change_email(self, session, collaborator_selected: User) -> User:
        """The function is used to change password of collaborator selected.

        Args:
            session (_type_): _description_
            collaborator_selected (User):Collaborator selected.
        Returns:
            User: Collaborator with new password.
        """
        section = f"Update/Changing the {collaborator_selected} email"
        self.generic_view.header(
            section=section, department=session.current_user_department, current_user=session.current_user.name
        )
        email = self.user_view._get_email(session=session)
        if self.generic_view.ask_comfirmation(message="Upadte Callaborator"):
            Manager().update_user(
                collaborator=collaborator_selected,
                update_attribute="email_adddress",
                new_value=email,
            )
            self.generic_view.confirmation_msg(
                session=session, section=" Update Collaborator", msg="Operation succesfull!"
            )
        else:
            self.generic_view.no_data_message(
                session=session, section=" Update Collaborator", msg="Operation Cancelled!"
            )

    @auth.is_authenticated
    def update_collaborator(self, session) -> User:
        """Function updates a collaborator.

        Returns:
            _type_: collaborator updated.
        """
        collaborator_selected = self.select_collaborator(session=session)
        if collaborator_selected != None:
            attribute_selected = self.utils._select_attribut_of_element(
                session=session,
                section="Update Collaborator/Select Attribute to updated",
                element=collaborator_selected,
            )
            if attribute_selected == "department":
                self.change_collaborator_department(session=session, collaborator_selected=collaborator_selected)
            elif attribute_selected == "password":
                self.change_password(session=session, collaborator_selected=collaborator_selected)
            elif attribute_selected == "email_address":
                self.change_email(session=session, collaborator_selected=collaborator_selected)
            else:
                self.change_collaborator_attribute(
                    session=session, collaborator_selected=collaborator_selected, attribute_selected=attribute_selected
                )
        else:
            self.generic_view.no_data_message(
                session=session,
                section="Upadte Collaborator",
                msg="There are no availble Collaborator. Update is not possible!",
            )

    @auth.is_authenticated
    def select_contract(self, session) -> Contract:
        """The function is used to select a Contract.

        Returns:
            Contract: Contract selected.
        """
        contracts = Manager().get_all_contracts(session=session)
        if len(contracts) > 0:
            contract_selected = self.utils._select_element_in_list(
                session=session, section="Update Contract/Select Contract", element_list=contracts
            )
            return contract_selected
        else:
            return None

    @auth.is_authenticated
    def change_customer_of_contract(self, session, contract_selected: Contract) -> Contract:
        """the function is used to change customer of contract, after selected a new customer by user.

        Args:
            session (_type_): _description_
            contract_selected (Contract): Contract to be updated.

        Returns:
            Contract: Contract updated.
        """
        section = " Update Contract"
        new_customer = self.select_customer_of_contract(session=session)
        if new_customer is None:
            self.generic_view.no_data_message(
                session=session,
                section=section,
                msg="There are no availble Customer. Update Contract is not possible!",
            )
        else:
            if self.generic_view.ask_comfirmation(message=section):
                Manager().update_contract(
                    contract=contract_selected, attribute_update="customer", new_value=new_customer
                )
                self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")
            else:
                self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def change_attribute_contract(self, session, attribute_selected: str, contract_selected: Contract) -> None:
        """The function is used to change attribute of contract selected.

        Args:
            session (_type_): _description_
            attribute_selected (str): attribute to be updated.
            contract_selected (Contract): contract to be updates.
        """
        section = " Update Contract"
        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=contract_selected,
            attribute_selected=attribute_selected,
        )
        if self.generic_view.ask_comfirmation(message=section):
            Manager().update_contract(
                contract=contract_selected, attribute_update=attribute_selected, new_value=new_value
            )
            self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")
        else:
            self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def update_contract(self, session) -> Contract:
        """The function is used to update a contract.

        Args:
            session (_type_): _description_

        Returns:
            Contract: Contract updated.
        """
        contract = self.select_contract(session=session)
        if contract != None:
            attribute_selected = self.utils._select_attribut_of_element(
                session=session, section=" Update Contract/Select Attribute to updated", element=contract
            )
            if attribute_selected == "customer":
                self.change_customer_of_contract(session=session, contract_selected=contract)
            else:
                self.change_attribute_contract(
                    session=session, attribute_selected=attribute_selected, contract_selected=contract
                )
        else:
            self.generic_view.no_data_message(
                session=session,
                section="Update Contract",
                msg="There are no availble contract. Update is not possible!",
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
        if len(supporters) > 0:
            supporter = self.utils._select_element_in_list(
                session=session, section="Update Event/ Select new Supporter", element_list=supporters
            )
            return supporter
        else:
            return None

    @auth.is_authenticated
    def select_event(self, session) -> Event:
        """the function is used to select an event.

        Args:
            session (_type_):sqlalchemy session

        Returns:
            Event: event selected.
        """
        events = Manager().get_all_events(session=session)
        if len(events) > 0:
            event = self.utils._select_element_in_list(
                session=session, section="Update/Select Event", element_list=events
            )
            return event
        else:
            return None

    @auth.is_authenticated
    def update_event(self, session):
        """The function change supporter of Event.

        Args:
            session (_type_): _description_
        """
        section = " Update event"
        event = self.select_event(session=session)
        supporter = self.select_supporter(session=session)
        if event is None or supporter is None:
            self.generic_view.no_data_message(
                session=session,
                section=section,
                msg="There are no available Event or Supporter. Update Event is not possible!",
            )
        else:
            if self.generic_view.ask_comfirmation(message=section):
                Manager().change_supporter_of_event(session=session, event=event, new_supporter=supporter)
                self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")
            else:
                self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def select_and_delete_collaborator(self, session, section: str, collaborator_list: list[User]):
        """The function is used to select and dlete user selected in list.

        Args:
            session (_type_): Sqlalchemy session
            section (str): Information to section to display in header.
            collaborator_list (list[User]): List of collaborator.
        """

        collaborator_selected = self.utils._select_element_in_list(
            session=session, section="Delete/ Select collobarator", element_list=collaborator_list
        )
        if self.generic_view.ask_comfirmation(message=section):
            Manager().delete_collaborator(session=session, collaborator_has_delete=collaborator_selected)
            self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")
        else:
            self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def delete_collaborator(self, session):
        """The function is used to delete a collaborator."""
        section = " Delete collaborator"
        collaborator_list = Manager().get_all_users(session=session)
        if len(collaborator_list) < 1 or collaborator_list == [session.current_user]:
            self.generic_view.no_data_message(
                session=session,
                section="Delete collaborator",
                msg="There are no available collaborator. Delete is not possible!",
            )
        else:
            collaborator_list.remove(session.current_user)
            self.select_and_delete_collaborator(session=session, section=section, collaborator_list=collaborator_list)
