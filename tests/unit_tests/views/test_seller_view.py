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

    def test_get_event_info_view(self, mocker):
        # test valid if dict returned is correct.
        mocker.patch("crm.view.generic_view.GenericView.header")
        event_restriction = [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "date_start", "parametre": {"type": "datetime", "max": None}},
            {"attribute_name": "date_end", "parametre": {"type": "datetime", "max": None}},
            {"attribute_name": "attendees", "parametre": {"type": int, "max": None}},
            {"attribute_name": "note", "parametre": {"type": str, "max": 2048}},
        ]
        mocker.patch("crm.models.element_administratif.Event.availables_attribue_list", return_value=event_restriction)
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="a string")
        mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value=1234)
        mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="a date")
        result = SellerView().get_event_info_view(department="", current_user_name="")
        assert result.get("name") == "a string"
        assert result.get("date_start") == "a date"
        assert result.get("date_end") == "a date"
        assert result.get("attendees") == 1234
        assert result.get("note") == "a string"

        assert len(result.keys()) == len(event_restriction)
