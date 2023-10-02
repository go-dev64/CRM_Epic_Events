import pytest
from pytest_mock import mocker
from sqlalchemy import select
from crm.models.element_administratif import Address
from crm.models.utils import Utils


class TestUtils:
    def test_get_type_of_user_with_manager(self, db_session, users, current_user_is_manager):
        u = Utils()
        with db_session as session:
            users
            current_user_is_manager
            assert u.get_type_of_user(session.current_user) == "Manager"

    def test_get_type_of_user_with_seller(self, db_session, users, current_user_is_seller):
        u = Utils()
        with db_session as session:
            users
            current_user_is_seller
            assert u.get_type_of_user(session.current_user) == "Seller"

    def test_get_type_of_user_with_supporter(self, db_session, users, current_user_is_supporter):
        u = Utils()
        with db_session as session:
            users
            current_user_is_supporter
            assert u.get_type_of_user(session.current_user) == "Supporter"

    def test_create_new_address(self, db_session, users, current_user_is_user, address, mocker):
        # test should return a new address.
        u = Utils()
        with db_session as session:
            users
            address
            current_user_is_user
            address_info = {
                "number": 1,
                "street": "address_info",
                "city": "city",
                "postal_code": 135,
                "country": "country",
                "note": "note",
            }
            mocker.patch("crm.view.generic_view.GenericView.get_address_info_view", return_value=address_info)
            u.create_new_address(session=session)
            list_address = session.scalars(select(Address)).all()
            assert len(list_address) == 2

    def test_select_address(self, db_session, users, current_user_is_user, address, mocker):
        with db_session as session:
            users
            address
            current_user_is_user
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=0)
            result = Utils().select_address(session=session)
            assert result == address

    @pytest.mark.parametrize(
        "attribute, new_value",
        [
            ("number", 123),
            ("street", "toto"),
            ("city", "trttg"),
            ("postal_code", 132),
            ("country", "vER"),
            ("note", "fbdf"),
        ],
    )
    def test_update_address(self, db_session, users, current_user_is_user, address, mocker, attribute, new_value):
        with db_session as session:
            users
            address
            current_user_is_user
            mocker.patch("crm.models.utils.Utils.select_address", return_value=address)
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            result = Utils().update_address(session=session)
            assert getattr(address, attribute) == new_value

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_select_element_in_list(self, db_session, users, current_user_is_manager, choice, mocker):
        liste_a = [1, 2, 3, 4, 5]
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            result = Utils()._select_element_in_list(session=session, section="", element_list=liste_a)
            assert result == liste_a[choice]

    @pytest.mark.parametrize("choice", [(0), (1), (2), (3)])
    def test_select_attribut_of_element(self, db_session, users, current_user_is_manager, choice, mocker):
        with db_session as session:
            users
            current_user_is_manager
            updatable_attribute_list = [x["attribute_name"] for x in users[0].availables_attribue_list()]
            mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view", return_value=choice)
            result = Utils()._select_attribut_of_element(session=session, section="", element=users[1])
            assert result == updatable_attribute_list[choice]
