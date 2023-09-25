from crm.models.authentication import Authentication
from crm.models.utils import Utils
from crm.view.customer_view import CustomerView
from crm.view.event_view import EventView
from crm.view.generic_view import GenericView


class SellerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.customer_view = CustomerView()
        self.event_view = EventView()
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
            choice = self.generic_view.select_element_view()
            match choice:
                case 1:
                    return self.create_new_customer(session=session)
                case 2:
                    return self.create_new_event(session=session)
                case 3:
                    return self.utils.create_new_address(session=session)
                case 4:
                    break

    @auth.is_authenticated
    def create_new_customer(self, session):
        """
        Function will create a new customer with the information entered by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: a new instance of Customer class.
        """
        customer_info = self.customer_view.get_info_customer()
        new_customer = session.current_user.create_new_customer(session=session, customer_info=customer_info)
        return new_customer

    @auth.is_authenticated
    def create_new_event(self, session):
        """
        Function will create a new event with the information entered by user.

        Args:
            session (_type_): _description_

        Returns:
            _type_: a new instance of Event class.
        """

        event_info = self.event_view.get_event_info()
        new_event = session.current_user.create_new_event(session=session, event_info=event_info)
        return new_event

    @auth.is_authenticated
    def select_customer_type_to_display(self, session):
        """
        Function redirect to other function according to current user's choice:
        - Display all customers .
        - Display customers handling by current user.


        Args:
            session (_type_): _description_

        Returns:
            _type_: elment selected. (customer)
        """
        choice_list = ["Select all customers", "Select yours customers"]
        choice = self.generic_view.select_element_view(list_element=choice_list)
        match choice:
            case 0:
                customer_list = session.current_user.get_all_customers(session=session)
                return self.generic_view.display_element(customer_list)
            case 1:
                yours_customers_list = session.current_user.get_all_clients_of_user(session)
                return self.generic_view.display_element(yours_customers_list)

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
        ]
        while True:
            choice = self.generic_view.select_element_view(list_element=choice_list)

            match choice:
                case 0:
                    contract_list = session.current_user.get_all_contracts(session=session)
                    return self.generic_view.display_element(contract_list)
                case 1:
                    yours_contract_list = session.current_user.get_all_contracts_of_user(session)
                    return self.generic_view.display_element(yours_contract_list)
                case 2:
                    unpayed_contracts_list = session.current_user.get_unpayed_contracts(session)
                    return self.generic_view.display_element(unpayed_contracts_list)
                case 3:
                    unsigned_contracts_list = session.current_user.get_unsigned_contracts(session)
                    return self.generic_view.display_element(unsigned_contracts_list)
                case 4:
                    element_list = session.current_user.get_all_contracts_of_user_without_event(session)
                    return self.generic_view.display_element(element_list)
                case 5:
                    break

    @auth.is_authenticated
    def update_seller_customer(self, session):
        """
        Function make update of customer of seller.
        """
        user_customer_list = session.current_user.get_all_clients_of_user(session=session)
        customer = self.utils._select_element_in_list(element_list=user_customer_list)
        attribute_selected = self.utils._select_attribut_of_element(element=customer)
        new_value = self.utils._get_new_value_of_attribut(element=customer, attribute_to_updated=attribute_selected)
        session.current_user.update_customer(
            session=session, customer=customer, attribute_update=attribute_selected, new_value=new_value
        )

    @auth.is_authenticated
    def update_seller_contract(self, session):
        """
        Function make update of contract of seller.
        """
        contracts_of_seller = session.current_user.get_all_contracts_of_user(session=session)
        contract = self.utils._select_element_in_list(element_list=contracts_of_seller)
        attribute_to_update = self.utils._select_attribut_of_element(element=contract)
        new_value = self.utils._get_new_value_of_attribut(element=contract, attribute_to_updated=attribute_to_update)
        session.current_user.update_contract(
            session=session, contract=contract, attribute_update=attribute_to_update, new_value=new_value
        )

    @auth.is_authenticated
    def select_element_type_to_be_updated(self, session):
        # select element type in list an retrun fuction to updated element.
        element_list = ["Update your customer", "Update your contracts", "Back"]
        while True:
            element_selected = self.generic_view.select_element_view(element_list)
            match element_selected:
                case 0:
                    # Update a user's customers.
                    return self.update_seller_customer(session=session)
                case 1:
                    # update a user's contract.
                    return self.update_seller_contract(session=session)
                case 2:
                    return self.utils.update_address(session=session)
                case 3:
                    break
