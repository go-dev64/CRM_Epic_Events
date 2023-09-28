import pytest
from crm.view.user_view import UserView
import argon2


class TestUserView:
    def test_get_user_info_view(self, mocker):
        mocker.patch("crm.view.generic_view.GenericView.header")
        user_restriction = [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 10}},
        ]
        mocker.patch("crm.models.users.User.availables_attribue_list", return_value=user_restriction)
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="astringg")
        mocker.patch("crm.view.user_view.UserView._get_user_password", return_value="password")
        result = UserView().get_user_info_view(section="", department="", current_user_name="")
        assert result.get("name") == "astringg"
        assert result.get("email_address") == "astringg"
        assert result.get("phone_number") == "astringg"
        assert result.get("password") == "password"
        assert len(result.keys()) == 4

    def test__get_user_password(self, mocker):
        mocker.patch("crm.view.generic_view.GenericView._input_password", return_value="password")
        mocker.patch("rich.prompt.Prompt.ask", return_value="password")
        result = UserView()._get_user_password()
        ph = argon2.PasswordHasher()
        assert ph.verify(result, "password")

    def test_get_user_password_with_bad_password(self, mocker, capsys):
        mocker.patch("crm.view.generic_view.GenericView._input_password", return_value="password")
        mock = mocker.patch("rich.prompt.Prompt.ask")
        mock.side_effect = ["toto", "password"]
        UserView()._get_user_password()
        out, err = capsys.readouterr()
        assert "Ouups your first password is different" in out
