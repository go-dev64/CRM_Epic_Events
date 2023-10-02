from datetime import datetime
import re
import pytest
from crm.models import users
from crm.view.generic_view import GenericView
from crm.models.users import Manager, Seller, Supporter
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.prompt import Confirm


class TestGenericView:
    def test_set_section(self):
        # test check the contents of section.
        section = "une section"
        result = GenericView().set_section(section)
        result_expected = f"Section:{section}"
        result = "".join(result._text)
        assert result == result_expected

    def test_set_department(self):
        deaprtement = "une section"
        result = GenericView().set_department(deaprtement)
        result_expected = f"Department:{deaprtement}"
        result = "".join(result._text)
        assert result == result_expected

    def test_set_currenut_user(self):
        # test check the contents of current user.
        element = "une element"
        result = GenericView().set_current_user(element)
        result_expected = f"User Connected:{element}"
        result = "".join(result._text)
        assert result == result_expected

    def test_element_renderable(self, mocker):
        # test check the contents of element_renderable.
        mocker.patch("crm.view.generic_view.GenericView.set_section", return_value="une section")
        mocker.patch("crm.view.generic_view.GenericView.set_department", return_value="une department")
        mocker.patch("crm.view.generic_view.GenericView.set_current_user", return_value="une user")
        elements = GenericView().set_element_renderable(section="", department="", current_user="")
        assert len(elements) == 3
        assert elements[0].renderable == "une section"
        assert elements[1].renderable == "une department"
        assert elements[2].renderable == "une user"

    def test_headers(self, mocker, capsys):
        # test checkthe contents of headers.
        element = [Panel("une section"), Panel("un departement"), Panel("un user")]
        mocker.patch("crm.view.generic_view.GenericView.set_element_renderable", return_value=element)
        GenericView().header()
        out, err = capsys.readouterr()
        assert "CRM Epic Event" in out
        assert "une section" and "un departement" and "un user" in out

    def test_display_element_list(self, mocker, capsys):
        # test check if the elements are displayed.
        mocker.patch("crm.view.generic_view.GenericView.header")
        list_element = ["element 1", " element 2", "element 3"]
        GenericView().display_element_list(section="", department="", current_user_name=",", list_element=list_element)
        out, err = capsys.readouterr()
        for i in list_element:
            assert i in out

    def test__set_table(self, capsys):
        attributes = ["name", "email_address", "phone_number"]
        result = GenericView()._set_table(title_table="test", attributes=attributes)
        assert len(result.columns) == len(attributes) + 1  # +1 is column of numero of row.
        assert "N°" == result.columns[0].header
        assert "name" == result.columns[1].header
        assert "email_address" == result.columns[2].header
        assert "phone_number" == result.columns[3].header

    def test_display_table_of_elements(self, capsys, mocker, db_session, users):
        with db_session as session:
            users
            attributes = users[0].attribute_to_display()
            toto = GenericView().display_table_of_elements(
                section="",
                department="",
                current_user_name="",
                title_table="test_title",
                list_element=users,
                attributes=attributes,
            )
            out, err = capsys.readouterr()
            print(out)
            assert "test_title" and "name" and "email_address" and "phone_number" and "N°" in out

    @pytest.mark.parametrize("result", [(1), (2)])
    def test__select_element_in_list(self, mocker, result):
        # test should return a index of chosen element in list of elements.
        mocker.patch("rich.prompt.IntPrompt.ask", return_value=result)
        list_element = ["element 1", " element 2", "element 3"]
        resultat = GenericView()._select_element_in_list(list_element=list_element)
        assert resultat == result - 1

    def test__select_element_in_list_with_bad_input(self, mocker, capsys):
        # test should return a msg error for input outside condition.
        mock = mocker.patch("rich.prompt.IntPrompt.ask")
        mock.side_effect = [5, 1]
        list_element = ["element 1", " element 2", "element 3"]
        GenericView()._select_element_in_list(list_element=list_element)
        out, err = capsys.readouterr()
        assert out == f"💩 Number must be between 1 and 3\n"

    @pytest.mark.parametrize("result", [(1), (2), (3)])
    def test_select_element_in_menu_view(self, mocker, result):
        # test should return a index of chosen element in list of elements.
        mocker.patch("crm.view.generic_view.GenericView.display_element_list")
        mocker.patch("crm.view.generic_view.GenericView._select_element_in_list", return_value=result - 1)
        list_element = ["element 1", " element 2", "element 3"]
        resultat = GenericView().select_element_in_menu_view(
            section="", department="", current_user_name=",", list_element=list_element
        )
        assert resultat == result - 1

    def test_choice_display_details_of_element(self, mocker):
        mocker.patch("rich.prompt.Confirm.ask", return_value=True)
        mocker.patch("crm.view.generic_view.GenericView._select_element_in_list", return_value=1)
        result = GenericView().choice_display_details_of_element(element_list=[1, 2, 3, 4, 5, 6])
        assert result == 1

    def test_choice_display_details_of_element_false(self, mocker):
        mocker.patch("rich.prompt.Confirm.ask", return_value=False)
        mocker.patch("crm.view.generic_view.GenericView._select_element_in_list", return_value=1)
        result = GenericView().choice_display_details_of_element(element_list=[1, 2, 3, 4, 5, 6])
        assert result == False

    def test_display_elements(self, mocker, db_session, clients, current_user_is_user, capsys):
        with db_session as session:
            clients
            current_user_is_user
            mocker.patch("crm.view.generic_view.GenericView.display_table_of_elements")
            mocker.patch("crm.view.generic_view.GenericView.display_detail_element")
            mocker.patch("crm.view.generic_view.GenericView.choice_display_details_of_element", return_value=1)
            result = GenericView().display_elements(
                session, elements_list=clients, session=session, title_table="", attributes="", msg=""
            )
            assert result == 1

    def test_display_detail_element_with_customer(self, mocker, db_session, clients, current_user_is_user, capsys):
        # test dislpay customer details.
        with db_session as session:
            clients
            current_user_is_user
            attributes = clients[0].attribute_to_display()
            mocker.patch("rich.prompt.Confirm.ask", return_value=True)
            GenericView().display_detail_element(session=session, element=clients[0], section="")
            out, err = capsys.readouterr()
            for i in attributes:
                assert i in out

    def test_display_detail_element_with_contract(self, mocker, db_session, contracts, current_user_is_user, capsys):
        # test dislpay customer details.
        with db_session as session:
            contracts
            current_user_is_user
            attributes = contracts[0].attribute_to_display()
            mocker.patch("rich.prompt.Confirm.ask", return_value=True)
            GenericView().display_detail_element(session=session, element=contracts[0], section="")
            out, err = capsys.readouterr()
            for i in attributes:
                assert i in out

    def test_display_detail_element_with_event(self, mocker, db_session, events, current_user_is_user, capsys):
        # test dislpay customer details.
        with db_session as session:
            events
            current_user_is_user
            attributes = events[0].attribute_to_display()
            mocker.patch("rich.prompt.Confirm.ask", return_value=True)
            GenericView().display_detail_element(session=session, element=events[0], section="")
            out, err = capsys.readouterr()
            for i in attributes:
                assert i in out

    def test_display_detail_element_with_manager(self, mocker, db_session, users, current_user_is_manager, capsys):
        # test dislpay manager details.
        with db_session as session:
            users
            current_user_is_manager
            attributes = users[0].attribute_to_display()
            mocker.patch("rich.prompt.Confirm.ask", return_value=True)
            GenericView().display_detail_element(session=session, element=users[0], section="")
            out, err = capsys.readouterr()
            for i in attributes:
                assert i in out

    def test_display_detail_element_with_address(
        self, mocker, db_session, users, address, current_user_is_manager, capsys
    ):
        # test dislpay address details.
        with db_session as session:
            users
            address
            current_user_is_manager
            attributes = address.attribute_to_display()
            mocker.patch("rich.prompt.Confirm.ask", return_value=True)
            GenericView().display_detail_element(session=session, element=address, section="")
            out, err = capsys.readouterr()
            for i in attributes:
                assert i in out

    def test_string_form(self, mocker):
        # test should return input if his respect condition(input < 50).
        restriction = {"attribute_name": "name", "parametre": {"type": str, "max": 50}}
        mocker.patch("rich.prompt.Prompt.ask", return_value="une string")
        result = GenericView().string_form(restriction=restriction)
        assert result == "une string"

    def test_string_form_with_bad_input(self, mocker, capsys):
        # test should return msg "name is toll long  with input > 2).
        mock = mocker.patch("rich.prompt.Prompt.ask")
        mock.side_effect = ["une string", "a"]
        restriction = {"attribute_name": "name", "parametre": {"type": str, "max": 2}}
        GenericView().string_form(restriction=restriction)
        out, err = capsys.readouterr()
        assert out == f"name too long\n\n"

    def test_integer_form(self, mocker):
        # test should return input if his respect condition(input < 50).
        restriction = {"attribute_name": "attendees", "parametre": {"type": int, "max": 50}}
        mocker.patch("rich.prompt.IntPrompt.ask", return_value=12)
        result = GenericView().integer_form(restriction=restriction)
        assert result == 12

    def test_string_form_with_bad_input(self, mocker, capsys):
        # test should return msg "name is toll long  with input > 10).
        mock = mocker.patch("rich.prompt.IntPrompt.ask")
        mock.side_effect = [55, 3]
        restriction = {"attribute_name": "attendees", "parametre": {"type": int, "max": 10}}
        GenericView().integer_form(restriction=restriction)
        out, err = capsys.readouterr()
        assert out == f"Number must be between 0 and 10\n"

    def test__input_password(self, mocker):
        # test check if password entered is valid. Should return value entered.
        mocker.patch("rich.prompt.Prompt.ask", return_value="password")
        mocker.patch("crm.models.authentication.Authentication._password_validator", return_value=True)
        result = GenericView()._input_password()
        assert result == "password"

    def test__input_password_with_bad_password(self, mocker, capsys):
        # test check if password entered is valid. Should return error message.
        mocker.patch("rich.prompt.Prompt.ask", return_value="password")
        mock = mocker.patch("crm.models.authentication.Authentication._password_validator")
        mock.side_effect = [None, True]
        GenericView()._input_password()
        out, err = capsys.readouterr()
        assert "Invalid password" in out

    def test_get_address_info_view(self, mocker):
        # test should return a new adrress.
        mocker.patch("crm.view.generic_view.GenericView.header")
        restrictions = [
            {"attribute_name": "number", "parametre": {"type": int, "max": None}},
            {"attribute_name": "street", "parametre": {"type": str, "max": 500}},
            {"attribute_name": "city", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "postal_code", "parametre": {"type": int, "max": None}},
            {"attribute_name": "country", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "note", "parametre": {"type": str, "max": 2048}},
        ]
        mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value=21)
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="string")
        result = GenericView().get_address_info_view(department="", current_user_name="")
        assert result.get("number") == 21
        assert result.get("street") == "string"
        assert result.get("city") == "string"
        assert result.get("postal_code") == 21
        assert result.get("country") == "string"
        assert result.get("note") == "string"
        assert len(result.keys()) == len(restrictions)

    def test_get_date(self, mocker):
        # test check if is datetime.
        mocker.patch("rich.prompt.Prompt.ask", return_value="10-10-2020")
        result = GenericView().get_date(msg="")
        assert type(result) == datetime

    def test_get_date_with_bad_input(self, mocker, capsys):
        # test should return error msg.
        mock = mocker.patch("rich.prompt.Prompt.ask")
        mock.side_effect = ["toto", "10-10-2020"]
        result = GenericView().get_date(msg="")
        out, err = capsys.readouterr()
        assert "Format date invalid" in out

    def test_get_hour(self, mocker):
        # test valid if is hour datetime.
        mocker.patch("rich.prompt.Prompt.ask", return_value="10")
        result = GenericView().get_hour(msg="")
        assert type(result) == datetime

    def test_get_hour_with_bad_input(self, mocker, capsys):
        # test should return error msg.
        mock = mocker.patch("rich.prompt.Prompt.ask")
        mock.side_effect = ["toto", "10"]
        result = GenericView().get_hour(msg="")
        out, err = capsys.readouterr()
        assert "Format hour invalid" in out

    def test_date_validator(self, mocker):
        # test valid if input iss greater than today.
        date = datetime.strptime("10-10-2023", "%d-%m-%Y")
        mocker.patch("crm.view.generic_view.GenericView.get_date", return_value=date)
        result = GenericView().date_validator(msg="")
        assert type(result) == datetime

    def test_date_validator_with_bad_input(self, mocker, capsys):
        # test should return error msg with date earlier than today.
        date = datetime.strptime("10-10-2023", "%d-%m-%Y")
        bad_date = datetime.strptime("10-10-2022", "%d-%m-%Y")
        mock = mocker.patch("crm.view.generic_view.GenericView.get_date")
        mock.side_effect = [bad_date, date]
        GenericView().date_validator(msg="")
        out, err = capsys.readouterr()
        assert "the date must be greater than today." in out

    def test_date_form(self, mocker):
        # test return a datetime.
        date = datetime.strptime("10-10-2023", "%d-%m-%Y")
        mock = mocker.patch("crm.view.generic_view.GenericView.get_date")
        mock.side_effect = [date]
        hour = datetime.strptime("10", "%H")
        mock1 = mocker.patch("crm.view.generic_view.GenericView.get_hour")
        mock1.side_effect = [hour]
        result = GenericView().date_form(msg="")
        assert result == datetime(2023, 10, 10, 10, 0)

    @pytest.mark.parametrize("attribute", [("name"), ("email_address"), ("phone_number"), ("password")])
    def test_get_new_value_of_attribute_for_user(self, mocker, db_session, users, current_user_is_manager, attribute):
        with db_session as session:
            users
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="value")

            result = GenericView().get_new_value_of_attribute(
                section="", department="", current_user="", element=users[0], attribute_selected=attribute
            )
            assert result == "value"

    @pytest.mark.parametrize("attribute", [("total_amount"), ("remaining"), ("signed_contract")])
    def test_get_new_value_of_attribute_for_contract(
        self, mocker, db_session, users, current_user_is_manager, contracts, attribute
    ):
        with db_session as session:
            users
            contracts
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="value")

            result = GenericView().get_new_value_of_attribute(
                section="", department="", current_user="", element=contracts[0], attribute_selected=attribute
            )
            assert result == "value"

    @pytest.mark.parametrize("attribute", [("name"), ("date_start"), ("date_end"), ("attendees"), ("note")])
    def test_get_new_value_of_attribute_for_event(
        self, mocker, db_session, users, current_user_is_manager, events, attribute
    ):
        with db_session as session:
            users
            events
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="value")

            result = GenericView().get_new_value_of_attribute(
                section="", department="", current_user="", element=events[0], attribute_selected=attribute
            )
            assert result == "value"

    @pytest.mark.parametrize("attribute", [("number"), ("street"), ("city"), ("postal_code"), ("country"), ("note")])
    def test_get_new_value_of_attribute_for_address(
        self, mocker, db_session, users, current_user_is_manager, address, attribute
    ):
        with db_session as session:
            users
            address
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="value")

            result = GenericView().get_new_value_of_attribute(
                section="", department="", current_user="", element=address, attribute_selected=attribute
            )
            assert result == "value"

    @pytest.mark.parametrize("attribute", [("name"), ("email_address"), ("phone_number"), ("company")])
    def test_get_new_value_of_attribute_for_customer(
        self, mocker, db_session, users, current_user_is_manager, clients, attribute
    ):
        with db_session as session:
            users
            clients
            current_user_is_manager
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.bool_form", return_value="value")
            mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="value")

            result = GenericView().get_new_value_of_attribute(
                section="", department="", current_user="", element=clients[0], attribute_selected=attribute
            )
            assert result == "value"
