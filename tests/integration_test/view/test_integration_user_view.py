import pytest
from crm.view.user_view import UserView


class TestIntUserView:
    """
    test integration of user_view module.
    """

    def test_get_user_info_view(self, mocker):
        # test valid if dict returned is correct.
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="astringg")
        mocker.patch("crm.view.user_view.UserView._get_user_password", return_value="password")
        result = UserView().get_user_info_view(section="", department="", current_user_name="")
        assert result.get("name") == "astringg"
        assert result.get("email_address") == "astringg"
        assert result.get("phone_number") == "astringg"
        assert result.get("password") == "password"
        assert len(result.keys()) == 4
