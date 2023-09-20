from crm.models.authentication import Authentication
from crm.view.generic_view import GenericView


class ManagerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()

    @auth.is_authenticated
    def create_new_element(self, session):
        while True:
            choice = self.generic_view.select_element_view()
            match choice:
                case 1:
                    return self.create_new_user(session=session)
                case 2:
                    return self.create_new_contract(session=session)
                case 3:
                    break

    @auth.is_authenticated
    def create_new_user(self, session):
        print("get info user")
        user_info = "input"
        print("select department")
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
    def create_new_contract(session):
        print("get info user")
        contract_info = "input"
        new_user = session.current_user.create_new_contract(session=session, contract_info=contract_info)
        return new_user
