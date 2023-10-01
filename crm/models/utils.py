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
        address_info = self.generic_view.get_address_info_view()
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

    def _select_element_in_list(self, session, section: str, element_list: list):
        """The function is used to select and return element in list.

        Args:
            session (_type_): session sqlalchemy
            section (str): Section information to be displayed in header.
            element_list (list): _description_

        Returns:
            _type_: element selected.
        """
        user_choice = self.generic_view.select_element_in_menu_view(
            section=section,
            department=session.current_user_department,
            current_user_name=session.current_user.name,
            list_element=element_list,
        )
        return element_list[user_choice]

    def _select_attribut_of_element(self, session, section, element):
        """
        Function used to select the attribute to be updated, in list, for the selected element.

        Returns:
            _type_: Return a attribute to be updated.
        """
        updatable_attribute_list = [x["attribute_name"] for x in element.availables_attribue_list()]
        user_choice = self.generic_view.select_element_in_menu_view(
            section=section,
            department=session.current_user_department,
            current_user_name=session.current_user.name,
            list_element=updatable_attribute_list,
        )
        return updatable_attribute_list[user_choice]
