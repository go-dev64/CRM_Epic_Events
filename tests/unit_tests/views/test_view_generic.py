import re
import pytest
from crm.view.generic_view import GenericView
from crm.models.users import Manager, Seller, Supporter
from rich.layout import Layout
from rich.panel import Panel


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
        mocker.patch("crm.view.generic_view.GenericView.display_element_list", return_value="")
        mocker.patch("rich.prompt.IntPrompt.ask", return_value=result)
        list_element = ["element 1", " element 2", "element 3"]
        resultat = GenericView().select_element_view(
            section="", department="", current_user_name=",", list_element=list_element
        )
        assert resultat == result - 1

    def test_select_element_view_with_bad_input(self, mocker, capsys):
        # test should return a msg error for input outside condition.
        mocker.patch("crm.view.generic_view.GenericView.display_element_list", return_value="")
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
        mocker.patch("rich.prompt.Prompt.ask", return_value="password")
        mocker.patch("crm.models.authentication.Authentication._password_validator", return_value=True)
        result = GenericView()._input_password()
        assert result == "password"

    def test__input_password_with_bad_password(self, mocker, capsys):
        mocker.patch("rich.prompt.Prompt.ask", return_value="password")
        mock = mocker.patch("crm.models.authentication.Authentication._password_validator")
        mock.side_effect = [None, True]
        GenericView()._input_password()
        out, err = capsys.readouterr()
        assert "Invalid password" in out
