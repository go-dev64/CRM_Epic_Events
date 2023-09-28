import pytest
from crm.view.seller_view import SellerView


class TestIntSellerView:
    def test_get_info_customer_view(self, mocker):
        # test valid if dict returned is correct.
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="a string")
        result = SellerView().get_info_customer_view(department="", current_user_name="")
        assert result.get("name") == "a string"
        assert result.get("email_address") == "a string"
        assert result.get("phone_number") == "a string"
        assert result.get("company") == "a string"

        assert len(result.keys()) == 4
