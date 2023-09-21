from crm.models.authentication import Authentication
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
    def select_collaborator_in_list(self, session):
        """
        Function displays a collaborator according to user's choise in collaborators list.

        Args:
            session (_type_): Display collaborator information.
        """
        collaborator_list = session.current_user.get_all_users(session=session)
        return self.generic_view.display_element(collaborator_list)

    @auth.is_authenticated
    def display_event_without_supporter(self, session):
        """
        Function displays a event without supporter according to user's choise in collaborators list.

        Args:
            session (_type_): Display event information.
        """
        event_list = session.current_user.get_all_event_without_support(session=session)
        return self.generic_view.display_element(event_list)
