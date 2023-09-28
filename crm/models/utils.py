from sqlalchemy import select
from crm.models.authentication import Authentication
from crm.models.element_administratif import Address
from crm.view.generic_view import GenericView


class Utils:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()

    def get_type_of_user(self, user) -> str:
        """Return l type of user: "Manager", "Seller" or "Supporter"

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

    @auth.is_authenticated
    def update_address(self, session):
        # update address.
        # list address
        address_list = session.scalars(select(Address)).all()
        # select address
        address = self._select_element_in_list(element_list=address_list)
        # select attribute to update
        attribute = self._select_attribut_of_element(element=address)
        # new value of attibute
        new_value = self._get_new_value_of_attribut(attribute_to_updated=attribute, element=address)
        setattr(address, attribute, new_value)

    def _select_element_in_list(self, element_list: list):
        """
        Function enabling the current user to select a element in list:

        Returns:
            _type_: element chosen.
        """
        user_choice = self.generic_view.select_element_view(element_list)
        return element_list[user_choice]

    def _select_attribut_of_element(self, element):
        """
        Function used to select the attribute to be updated, in list, for the selected element.

        Returns:
            _type_: Return a attribute to be updated.
        """
        updatable_attribute_list = [x for x in element.availables_attribue_list().keys()]
        user_choice = self.generic_view.select_element_view(updatable_attribute_list)
        return updatable_attribute_list[user_choice]

    def _get_new_value_of_attribut(self, element, attribute_to_updated):
        """
        function get a new value of element.

        Args:
            element (_type_): element to be updated
            attribute_to_updated (_type_): attribute of element to be updated.

        Returns:
            _type_: new value of attribute.
        """
        restriction = element.availables_attribue_list()[attribute_to_updated]
        new_value = self.manager_view.get_new_value_of_customer_attribute(restriction=restriction)
        return new_value
