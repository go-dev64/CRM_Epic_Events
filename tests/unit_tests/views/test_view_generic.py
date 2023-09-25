import sys
import pytest
from crm.view.generic_view import GenericView
from rich.panel import Panel


class TestGenericView:
    def test_headers(self, capsys):
        section = "une section"
        GenericView().header(section)
        out, err = capsys.readouterr()
        assert "CRM Epic Event" and section in out
