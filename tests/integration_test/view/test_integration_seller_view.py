from crm.view.seller_view import SellerView


class TestIntSellerView:
    def test_get_info_customer_view(self, db_session, current_user_is_seller, mocker):
        # test valid if dict returned is correct.
        with db_session as session:
            current_user_is_seller
            mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="a string")
            mocker.patch("crm.view.seller_view.SellerView.get_customer_email", return_value="adssjjsjsqj@gmail.fr")
            result = SellerView().get_info_customer_view(session=session)
            assert result.get("name") == "a string"
            assert result.get("email_address") == "adssjjsjsqj@gmail.fr"
            assert result.get("phone_number") == "a string"
            assert result.get("company") == "a string"

        assert len(result.keys()) == 4

    def test_get_event_info_view(self, mocker):
        # test valid if dict returned is correct.
        mocker.patch("crm.view.generic_view.GenericView.string_form", return_value="a string")
        mocker.patch("crm.view.generic_view.GenericView.integer_form", return_value=1234)
        mocker.patch("crm.view.generic_view.GenericView.date_form", return_value="a date")
        result = SellerView().get_event_info_view(department="", current_user_name="")
        assert result.get("name") == "a string"
        assert result.get("date_start") == "a date"
        assert result.get("date_end") == "a date"
        assert result.get("attendees") == 1234
        assert result.get("note") == "a string"
