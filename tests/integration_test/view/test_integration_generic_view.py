import re
import pytest
from crm.view.generic_view import GenericView
from crm.models.users import Manager, Seller, Supporter
from rich.layout import Layout
from rich.panel import Panel


class TestIntGenericView:
    def test_element_renderable(self):
        # test should check the contents  of elements.
        elements = GenericView().set_element_renderable(
            section="une section", department="une department", current_user="une user"
        )
        assert len(elements) == 3
        assert "une section" in elements[0].renderable
        assert "une department" in elements[1].renderable
        assert "une user" in elements[2].renderable

    def test_headers(self, mocker, capsys):
        #  test should check the contents  of header.
        GenericView().header(section="une section", department="une department", current_user="une user")
        out, err = capsys.readouterr()
        assert "CRM Epic Event" and "une section" and "une department" and "une user" in out

    def test_display_element_list(self, mocker, capsys):
        # test check if the elements are displayed.
        list_element = ["element 1", " element 2", "element 3"]
        GenericView().display_element_list(section="", department="", current_user_name=",", list_element=list_element)
        out, err = capsys.readouterr()
        for i in list_element:
            assert i in out

    @pytest.mark.parametrize("result", [(1), (2), (3)])
    def test_select_element_view(self, mocker, result, capsys):
        # test should return a index of chosen element in list of elements.
        mocker.patch("rich.prompt.IntPrompt.ask", return_value=result)
        list_element = ["element 1", " element 2", "element 3"]
        resultat = GenericView().select_element_view(
            section="", department="", current_user_name=",", list_element=list_element
        )
        out, err = capsys.readouterr()
        assert resultat == result - 1
        assert "element 1" and " element 2" and "element 3" in out

    def test_select_element_view_with_bad_input(self, mocker, capsys):
        # test should return a msg error for input outside condition.
        mock = mocker.patch("rich.prompt.IntPrompt.ask")
        mock.side_effect = [5, 1]
        list_element = ["element 1", " element 2", "element 3"]
        GenericView().select_element_view(section="", department="", current_user_name=",", list_element=list_element)
        out, err = capsys.readouterr()
        assert f"💩 Number must be between 1 and 3\n" in out
        assert "element 1" and " element 2" and "element 3" in out

    def test__input_password(self, mocker):
        # test check if password entered is valid. Should return value entered.
        password = "Abcdefgh@120"
        mocker.patch("rich.prompt.Prompt.ask", return_value=password)
        result = GenericView()._input_password()
        assert result == password

    def test__input_password_with_bad_password(self, mocker, capsys):
        # test check if password entered is valid. Should return error message.
        mock = mocker.patch("rich.prompt.Prompt.ask")
        mock.side_effect = ["password", "Abcdefgh@120"]
        GenericView()._input_password()
        out, err = capsys.readouterr()
        assert "Invalid password" in out
