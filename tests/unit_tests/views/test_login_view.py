import pytest
from pytest_mock import mocker
from crm.view.login_view import LoginView
from unittest.mock import patch


class TestLoginView:
    def test_authentication_is_ok(self, capsys):
        LoginView().authentication_ok()
        out, err = capsys.readouterr()
        expected_out = "✅ Authentication is ok ✅\n"
        assert out == expected_out

    def test_get_user_email_and_password(self, capsys, mocker):
        mocker.patch("crm.view.login_view.LoginView.get_email", return_value="unemail@gmail.com")
        mocker.patch("crm.view.login_view.LoginView.get_password", return_value="un passport")
        result = LoginView().get_user_email_and_password()
        out, err = capsys.readouterr()
        assert "CRM Epic Event" and "Authentication" in out
        assert "unemail@gmail.com" == result[0]
        assert "un passport" == result[1]
