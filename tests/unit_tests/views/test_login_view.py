import pytest
from crm.view.login_view import LoginView
from email_validator import EmailNotValidError


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

    def test_get_email(self, mocker):
        mock_input = mocker.patch("rich.prompt.Prompt.ask")
        mock_input.side_effect = ["wright.email@gmail.com"]
        result = LoginView().get_email()
        assert result == "wright.email@gmail.com"

    def test_get_email_bad_mail(self, mocker, capsys):
        mock_input = mocker.patch("rich.prompt.Prompt.ask")
        mock_input.side_effect = ["badmail", "wright.email@gmail.com"]
        LoginView().get_email()
        out, err = capsys.readouterr()
        assert "The email address is not valid. It must have exactly one @-sign." in out
