from datetime import datetime
import pytest
from crm.controller.supporter_controller import SupporterController
from crm.models.element_administratif import Address
from crm.view.generic_view import GenericView


class TestSupportController:
    def test_display_all_events(self, db_session, users, current_user_is_supporter, mocker):
        # test should display events elements.
        with db_session as session:
            users
            current_user_is_supporter
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Supporter.get_all_events", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SupporterController().display_all_events(session=session)
            mock_display_elements.assert_called_once()

    def test_test_display_all_events_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_supporter
            element_list = []
            mocker.patch("crm.models.users.Supporter.get_all_events", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SupporterController().display_all_events(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_events_of_user(self, db_session, users, current_user_is_supporter, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_supporter
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Supporter.get_event_of_supporter", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SupporterController().display_all_events_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_test_display_all_events_of_user_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_supporter
            element_list = []
            mocker.patch("crm.models.users.Supporter.get_event_of_supporter", return_value=element_list)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SupporterController().display_all_events_of_user(session=session)
            mock_display_elements.assert_called_once()

    @pytest.mark.parametrize("choice", [(0), (1)])
    def test_display_event(self, db_session, users, current_user_is_supporter, mocker, choice):
        with db_session as session:
            users
            current_user_is_supporter
            mock_choice = mocker.patch("crm.view.generic_view.GenericView.select_element_in_menu_view")
            mock_choice.side_effect = [choice, 2]
            mock_all_event = mocker.patch.object(SupporterController, "display_all_events")
            mock_display_all_events_of_user = mocker.patch.object(SupporterController, "display_all_events_of_user")
            SupporterController().display_event(session=session)
            if choice == 0:
                mock_all_event.assert_called_once()
            elif choice == 1:
                mock_display_all_events_of_user.assert_called_once()

    def test_select_event(self, db_session, users, current_user_is_supporter, mocker):
        # test should return a good element choosen in list.
        with db_session as session:
            users
            current_user_is_supporter
            element_list = ["A", "B", "C"]
            mocker.patch("crm.models.users.Supporter.get_event_of_supporter", return_value=element_list)
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=0,
            )
            result = SupporterController().select_event(session=session)
            assert result == element_list[0]

    def test_select_event_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # test should return None.
        with db_session as session:
            users
            current_user_is_supporter
            element_list = []
            mocker.patch("crm.models.users.Supporter.get_event_of_supporter", return_value=element_list)

            result = SupporterController().select_event(session=session)
            assert result == None

    def test_change_addres_of_event(self, db_session, users, current_user_is_supporter, events, mocker):
        # test should return an event with new address.
        with db_session as session:
            users
            current_user_is_supporter
            address = Address(number=2, street="street", city="city", postal_code=1234, country="wftrt")
            session.add_all([address])
            session.commit()
            events
            mocker.patch(
                "crm.controller.seller_controller.SellerController.select_address_of_event", return_value=address
            )
            SupporterController().change_address_of_event(session=session, event_selected=events[0])
            assert events[0].address == address

    @pytest.mark.parametrize(
        "attribute,new_value",
        [
            ("name", "test"),
            ("date_start", datetime.now()),
            ("date_end", datetime.now()),
            ("attendees", 1234),
            ("note", "test note"),
        ],
    )
    def test_change_attribute_of_event(
        self, db_session, users, current_user_is_supporter, events, mocker, attribute, new_value
    ):
        with db_session as session:
            users
            current_user_is_supporter
            events
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            SupporterController().change_attribute_of_event(
                session=session, event_selected=events[0], attribute_selected=attribute
            )

            assert getattr(events[0], attribute) == new_value

    def test_update_element_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # Test should retrun a event updated.
        with db_session as session:
            users
            current_user_is_supporter
            mocker.patch("crm.controller.supporter_controller.SupporterController.select_event", return_value=None)
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SupporterController().update_element(session=session)
            mock_display_elements.assert_called_once()

    @pytest.mark.parametrize("choice", [("contract"), ("supporter")])
    def test_update_element_with_forbidden_attribute(
        self, db_session, users, current_user_is_supporter, events, mocker, choice
    ):
        with db_session as session:
            users
            current_user_is_supporter
            events
            mocker.patch(
                "crm.controller.supporter_controller.SupporterController.select_event", return_value=events[0]
            )
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=choice)
            mock_message = mocker.patch.object(GenericView, "forbidden_acces")
            SupporterController().update_element(session=session)
            mock_message.assert_called_once()

    def test_update_element_with_change_address(self, db_session, users, current_user_is_supporter, events, mocker):
        with db_session as session:
            users
            current_user_is_supporter
            events
            mocker.patch(
                "crm.controller.supporter_controller.SupporterController.select_event", return_value=events[0]
            )
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value="address")
            mock_change_address_of_event = mocker.patch.object(SupporterController, "change_address_of_event")
            SupporterController().update_element(session=session)
            mock_change_address_of_event.assert_called_once()

    @pytest.mark.parametrize("attribute", [("name"), ("date_start"), ("date_end"), ("attendees"), ("note")])
    def test_update_element_with_change_attribute(
        self, db_session, users, current_user_is_supporter, events, mocker, attribute
    ):
        with db_session as session:
            users
            current_user_is_supporter
            events
            mocker.patch(
                "crm.controller.supporter_controller.SupporterController.select_event", return_value=events[0]
            )
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mock_change_address_of_event = mocker.patch.object(SupporterController, "change_attribute_of_event")
            SupporterController().update_element(session=session)
            mock_change_address_of_event.assert_called_once()
