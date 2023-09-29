from datetime import datetime
import re
import pytest
from crm.view.generic_view import GenericView
from crm.models.users import Manager, Seller, Supporter
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console


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

    @pytest.mark.parametrize("result", [(1), (2), (3)])
    def test_select_element_view(self, mocker, result):
        # test should return a index of chosen element in list of elements.
        mocker.patch("crm.view.generic_view.GenericView.display_element_list")
        mocker.patch("rich.prompt.IntPrompt.ask", return_value=result)
        list_element = ["element 1", " element 2", "element 3"]
        resultat = GenericView().select_element_view(
            section="", department="", current_user_name=",", list_element=list_element
        )
        assert resultat == result - 1

    def test_select_element_view_with_bad_input(self, mocker, capsys):
        # test should return a msg error for input outside condition.
        mocker.patch("crm.view.generic_view.GenericView.display_element_list")
        mock = mocker.patch("rich.prompt.IntPrompt.ask")
        mock.side_effect = [5, 1]
        list_element = ["element 1", " element 2", "element 3"]
        GenericView().select_element_view(section="", department="", current_user_name=",", list_element=list_element)
        out, err = capsys.readouterr()
        assert out == f"💩 Number must be between 1 and 3\n"

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

    def test__set_table(self, capsys):
        restrictions = [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 10}},
        ]
        result = GenericView()._set_table(title_table="test", restrictions=restrictions)
        assert len(result.columns) == len(restrictions) + 1  # +1 is column of numero of row.
        assert "N°" == result.columns[0].header
        assert "name" == result.columns[1].header
        assert "email_address" == result.columns[2].header
        assert "phone_number" == result.columns[3].header

    def test_display_table_of_elements(self, capsys, mocker, db_session, users):
        with db_session as session:
            users
            restrictions = [
                {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
                {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
                {"attribute_name": "phone_number", "parametre": {"type": str, "max": 10}},
            ]
            toto = GenericView().display_table_of_elements(
                section="",
                department="",
                current_user_name="",
                title_table="test_title",
                list_element=users,
                restrictions=restrictions,
            )
            out, err = capsys.readouterr()
            assert "test_title" and "name" and "email_address" and "phone_number" and "N°" in out
