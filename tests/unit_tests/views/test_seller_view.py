import pytest
from crm.view.seller_view import SellerView


class TestSellerView:
    def test_get_info_customer_view(self, mocker):
        # test valid if dict returned is correct.
        mocker.patch("crm.view.generic_view.GenericView.header")
        customer_restriction = [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 255}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 255}},
            {"attribute_name": "company", "parametre": {"type": str, "max": 255}},
        ]
        mocker.patch("crm.models.customer.Customer.availables_attribue_list", return_value=customer_restriction)
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="a string")
        result = SellerView().get_info_customer_view(department="", current_user_name="")
        assert result.get("name") == "a string"
        assert result.get("email_address") == "a string"
        assert result.get("phone_number") == "a string"
        assert result.get("company") == "a string"

        assert len(result.keys()) == len(customer_restriction)
