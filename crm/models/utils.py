from crm.models.authentication import Authentication
from crm.view.generic_view import GenericView


class Utils:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()

    def get_type_of_user(self, user) -> str:
        """
        Return l type of user: "Manager", "Seller" or "Supporter"

        Args:
            user (_type_): Instance User class.

        Returns:
            str: "Manager", "Seller" or "Supporter"
        """
        user_type = type(user).__name__
        return user_type

    @auth.is_authenticated
    def create_new_address(self, session):
        address_info = self.generic_view.get_address_info()
        new_address = session.current_user.create_new_address(session=session, address_info=address_info)
        return new_address
