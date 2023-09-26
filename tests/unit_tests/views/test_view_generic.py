import re
import pytest
from crm.view.generic_view import GenericView
from crm.models.users import Manager, Seller, Supporter
from rich.layout import Layout
from rich.panel import Panel


class TestGenericView:
    def test_set_section(self):
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
        element = "une element"
        result = GenericView().set_current_user(element)
        result_expected = f"User Connected:{element}"
        result = "".join(result._text)
        assert result == result_expected

    def test_element_renderable(self, mocker):
        mocker.patch("crm.view.generic_view.GenericView.set_section", return_value="une section")
        mocker.patch("crm.view.generic_view.GenericView.set_department", return_value="une department")
        mocker.patch("crm.view.generic_view.GenericView.set_current_user", return_value="une user")
        elements = GenericView().set_element_renderable(section="", department="", current_user="")
        assert len(elements) == 3
        assert elements[0].renderable == "une section"
        assert elements[1].renderable == "une department"
        assert elements[2].renderable == "une user"

    def test_headers(self, mocker, capsys):
        element = [Panel("une section"), Panel("un departement"), Panel("un user")]
        mocker.patch("crm.view.generic_view.GenericView.set_element_renderable", return_value=element)
        GenericView().header()
        out, err = capsys.readouterr()
        assert "CRM Epic Event" in out
        assert "une section" and "un departement" and "un user" in out

    def test_display_element_list(self, mocker, capsys):
        mocker.patch("crm.view.generic_view.GenericView.header", return_value="")
        list_element = ["element 1", " element 2", "element 3"]
        GenericView().display_element_list(section="", department="", current_user_name=",", list_element=list_element)
        out, err = capsys.readouterr()
        for i in list_element:
            assert i in out

    @pytest.mark.parametrize("result", [(1), (2), (3)])
    def test_select_element_in_list(self, mocker, result):
        mocker.patch("crm.view.generic_view.GenericView.display_element_list", return_value="")
        mocker.patch("rich.prompt.IntPrompt.ask", return_value=result)
        list_element = ["element 1", " element 2", "element 3"]
        resultat = GenericView().select_element_view(
            section="", department="", current_user_name=",", list_element=list_element
        )
        assert resultat == result - 1

    def test_string_form(self, mocker):
        restriction = {"attribute_name": "name", "parametre": {"type": str, "max": 50}}
        mocker.patch("rich.prompt.Prompt.ask", return_value="une string")
        result = GenericView().string_form(restriction=restriction)
        assert result == "une string"
