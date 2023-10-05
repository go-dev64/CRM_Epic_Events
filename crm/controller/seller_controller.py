from crm.models.authentication import Authentication
from crm.models.customer import Customer
from crm.models.element_administratif import Address, Contract, Event
from crm.models.users import Seller, User
from crm.models.utils import Utils
from crm.view.seller_view import SellerView
from crm.view.event_view import EventView
from crm.view.generic_view import GenericView


class SellerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.seller_view = SellerView()
        self.utils = Utils()

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
            list_of_choice = [
                "Create a new Customer",
                "Create a new Event",
                "Create a new Address",
                "Back to previous menu",
            ]
            choice = self.generic_view.select_element_in_menu_view(
                section="Create Element: Choice",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=list_of_choice,
            )
            match choice:
                case 0:
                    self.create_new_customer(session=session)
                case 1:
                    self.create_new_event(session=session)
                case 2:
                    self.utils.create_new_address(session=session)
                case 3:
                    break

    @auth.is_authenticated
    def create_new_customer(self, session) -> Customer:
        """
        Function will create a new customer with the information entered by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: a new instance of Customer class.
        """
        section = " Create new Customer"
        customer_info = self.seller_view.get_info_customer_view(
            department=session.current_user_department, current_user_name=session.current_user.name
        )
        if self.generic_view.ask_comfirmation(message=section):
            new_customer = Seller().create_new_customer(session=session, customer_info=customer_info)
            self.generic_view.confirmation_msg(section=section, session=session, msg="Operation succesfull!")
            return new_customer
        else:
            self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def select_contract_of_event(self, session) -> Contract:
        """The function is used to select a contract in contract list for event.

        Args:
            session (_type_): Actual sqlalchemy session.

        Returns:
            Contract: contract selected by user.
        """
        contract_list = Seller().get_all_contracts_of_user_without_event(session=session)
        if len(contract_list) > 0:
            choice = self.generic_view.select_element_in_menu_view(
                section="Select Contract of Event",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=contract_list,
            )
            return contract_list[choice]
        else:
            return None

    @auth.is_authenticated
    def select_address_of_event(self, session) -> Address:
        """The function is used to select an address in address list for event.
        if no addres available is redireted to address creation function.

        Args:
            session (_type_): Actual sqlalchemy session.

        Returns:
            Address: Address selected by user.
        """
        section = "Select Address of Event"
        address_selected = self.utils.select_address(session=session)
        if address_selected is None:
            self.generic_view.no_data_message(
                session=session, section=section, msg="no address available, redirect to address creation"
            )
            new_address = self.utils.create_new_address(session=session)
            return new_address
        else:
            return address_selected

    def get_address_of_event(self, session):
        choice_list = ["Select address", "Create new address"]
        choice = self.generic_view.select_element_in_menu_view(
            section="Select Address of Event",
            department=session.current_user_department,
            current_user_name=session.current_user.name,
            list_element=choice_list,
        )
        match choice:
            case 0:
                self.select_address_of_event(session=session)
            case 1:
                self.utils.create_new_address(session=session)

    @auth.is_authenticated
    def get_event_info(self, session) -> dict:
        """The function is used to get event info for create a new event.

        Args:
            session (_type_): actual Sqlalchemy session.

        Returns:
            dict: event_info
        """
        event_info = self.seller_view.get_event_info_view(
            section="Create New event",
            department=session.current_user_department,
            current_user_name=session.current_user.name,
        )
        event_info["address"] = self.get_address_of_event(session=session)
        event_info["contract"] = self.select_contract_of_event(session=session)
        return event_info

    @auth.is_authenticated
    def create_new_event(self, session) -> Event:
        """Function will create a new event with the information entered by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: a new instance of Event class.
        """
        section = " Create New event"
        event_info = self.get_event_info(session=session)
        if event_info["contract"] != None:
            if self.generic_view.ask_comfirmation(message=section):
                new_event = Seller().create_new_event(session=session, event_info=event_info)
                self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")
                return new_event
            else:
                self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")
        else:
            self.generic_view.no_data_message(
                session=session,
                section=section,
                msg="There are no available contract. Create new Event is not possible!",
            )

    @auth.is_authenticated
    def display_all_customers(self, session):
        """The funtion is used to display all customers.
        display msg no data if there are no customers to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Customers"
        title_table = "Table of all customers"
        customer_list = Seller().get_all_customers(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_all_customersof_user(self, session):
        """The funtion is used to display all customers.
        display msg no data if there are no customers to display.

        Args:
            session (_type_): _description_
        """
        section = "Display your Customers"
        title_table = "Table of all your customers"
        customer_list = Seller().get_all_clients_of_user(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def select_customer_type_to_display(self, session):
        """
        Function redirect to other function according to current user's choice:
        - Display all customers .
        - Display customers handling by current user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: element selected. (customer)
        """
        choice_list = ["Select all customers", "Select yours customers", "Back to previous menu"]
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Display Customer/ Select elment to displayed",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=choice_list,
            )
            match choice:
                case 0:
                    self.display_all_customers(session=session)
                case 1:
                    self.display_all_customersof_user(session=session)
                case 2:
                    break

    @auth.is_authenticated
    def display_all_contracts(self, session):
        """The funtion is used to display all contracts.
        display msg no data if there are no contract to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Contracts"
        title_table = "Table of all contracts"
        customer_list = Seller().get_all_contracts(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_all_contracts_of_user(self, session):
        """The funtion is used to display all contracts managed by user.
        display msg no data if there are no contract to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Contracts"
        title_table = "Table of all contracts"
        customer_list = Seller().get_all_contracts_of_user(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_all_unpayed_contracts_of_user(self, session):
        """The funtion is used to display all unpayed contracts managed by current user.
        display msg no data if there are no contract to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Contracts"
        title_table = "Table of All Yours Unpayed Contracts"
        customer_list = Seller().get_unpayed_contracts(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_all_unsigned_contracts_of_user(self, session):
        """The funtion is used to display all unsigned contracts managed by user.
        display msg no data if there are no contract to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Contracts"
        title_table = "All Yours Unsigned Contracts"
        customer_list = Seller().get_unsigned_contracts(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_all_contracts_of_user_without_event(self, session):
        """The funtion is used to display all contracts without event managed by user.
        display msg no data if there are no contract to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Contracts"
        title_table = "All Yours signed Contracts availabes for events"
        customer_list = Seller().get_all_contracts_of_user_without_event(session=session)
        if len(customer_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=customer_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def select_contract_type_to_display(self, session):
        """
        Function redirect to other function according tu current user's choice:
        - Get all contracts and display the one selected by user.
        - Get all contracts hanlding by user and display the one selected by user.
        - Get all unpayed contracts hanlding by user and display the one selected by user.
        - Get all signed contracts hanlding by user and display the one selected by user.
        - Get all  contracts without event hanlding by user and display the one selected by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: _description_
        """
        choice_list = [
            "Display all contracts",
            "Display your contract",
            "Display your unpayed contracts",
            "Display your unsigned contract",
            "Display your contract signed without Event",
            "Back to previous menu",
        ]
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Display Contract/Select element to displayed",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=choice_list,
            )
            match choice:
                case 0:
                    self.display_all_contracts(session=session)
                case 1:
                    self.display_all_contracts_of_user(session=session)
                case 2:
                    self.display_all_unpayed_contracts_of_user(session=session)
                case 3:
                    self.display_all_unsigned_contracts_of_user(session=session)
                case 4:
                    self.display_all_contracts_of_user_without_event(session=session)
                case 5:
                    break

    @auth.is_authenticated
    def select_customer(self, session) -> Customer:
        """The function is used to select a Customer.

        Returns:
            Customer: Customer selected.
        """
        section = "Update your Customer/Select Customer"
        customers = Seller().get_all_clients_of_user(session=session)
        if len(customers) > 0:
            customer_selected = self.utils._select_element_in_list(
                session=session, section=section, element_list=customers
            )
            return customer_selected
        else:
            return None

    @auth.is_authenticated
    def change_attribute_of_customer(
        self, session, section: str, attribute_selected: str, customer_selected: Customer
    ) -> None:
        """The function is used to change attribute of customer selected.

        Args:
            session (_type_): Sqlalchemy session.
            section (str): section information to displayed in headers.
            attribute_selected (str): Attribute to be updated.
            customer_selected (Customer): Customer selected.
        """

        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=customer_selected,
            attribute_selected=attribute_selected,
        )
        if self.generic_view.ask_comfirmation(message=section):
            Seller().update_customer(
                session=session, customer=customer_selected, attribute_update=attribute_selected, new_value=new_value
            )
            self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")

        else:
            self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def update_seller_customer(self, session):
        """The function is used to update the customers managed by the current user.

        Args:
            session (_type_): _description_
        """
        section = " Update your Customer "
        customer = self.select_customer(session=session)
        if customer != None:
            attribute_selected = self.utils._select_attribut_of_element(
                session=session, section="Update your Customer/Select Attribute", element=customer
            )
            if attribute_selected == "seller_contact":
                self.generic_view.forbidden_acces(session=session, section=" Update your Customer")
            else:
                self.change_attribute_of_customer(
                    session=session, section=section, attribute_selected=attribute_selected, customer_selected=customer
                )
        else:
            self.generic_view.no_data_message(
                session=session, section="Update your Customer", msg="No customer available to updating!"
            )

    @auth.is_authenticated
    def select_contract(self, session) -> Contract:
        """The function is used to select a Contract.
        return None if contracts list is empty.

        Returns:
            Contract: Contract selected.
        """
        section = "Update your Contract/Select Contract"
        contracts = Seller().get_all_contracts_of_user(session=session)
        if len(contracts) > 0:
            contract_selected = self.utils._select_element_in_list(
                session=session, section=section, element_list=contracts
            )
            return contract_selected
        else:
            return None

    @auth.is_authenticated
    def change_attribute_of_contract(self, session, contract_selected):
        section = " Upadte Contract"
        attribute_selected = self.utils._select_attribut_of_element(
            session=session, section="Update your Contract/Select Attribute", element=contract_selected
        )
        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=contract_selected,
            attribute_selected=attribute_selected,
        )
        if self.generic_view.ask_comfirmation(message=section):
            Seller().update_contract(
                session=session, contract=contract_selected, attribute_update=attribute_selected, new_value=new_value
            )
            self.generic_view.confirmation_msg(session=session, section=section, msg="Operation succesfull!")

        else:
            self.generic_view.no_data_message(session=session, section=section, msg="Operation Cancelled!")

    @auth.is_authenticated
    def update_seller_contract(self, session):
        """
        Function make update of contract of seller.
        """
        section = " Upadte Contract"
        contract = self.select_contract(session=session)
        if contract != None:
            self.change_attribute_of_contract(session=session, contract_selected=contract)
        else:
            self.generic_view.no_data_message(
                session=session, section=section, msg="No contract available to updating!"
            )

    @auth.is_authenticated
    def select_element_type_to_be_updated(self, session):
        """The function is used to select an action in menu list.
        Choices are differents type of element to update.
        Retrun fuction to updated element

        Args:
            session (_type_): _description_

        Returns:
            _type_: Uppdate function for element choosen.
        """
        element_list = ["Update your customer", "Update your contracts", "Back"]
        while True:
            element_selected = self.generic_view.select_element_in_menu_view(
                section="Update/Select element to be updated",
                department=session.current_user_department,
                current_user_name=session.current_user.name,
                list_element=element_list,
            )
            match element_selected:
                case 0:
                    # Update a user's customers.
                    self.update_seller_customer(session=session)
                case 1:
                    # update a user's contract.
                    self.update_seller_contract(session=session)
                case 2:
                    # update address
                    self.utils.update_address(session=session)
                case 3:
                    break
