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
