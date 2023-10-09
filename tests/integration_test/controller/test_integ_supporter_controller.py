from crm.controller.supporter_controller import SupporterController
from crm.view.generic_view import GenericView


class TestIntSupporterController:
    def test_display_all_events(self, db_session, users, events, current_user_is_supporter, mocker):
        # test should display events elements.
        with db_session as session:
            users
            current_user_is_supporter
            events
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SupporterController().display_all_events(session=session)
            mock_display_elements.assert_called_once()

    def test_test_display_all_events_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_supporter
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SupporterController().display_all_events(session=session)
            mock_display_elements.assert_called_once()

    def test_display_all_events_of_user(self, db_session, users, current_user_is_supporter, events, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_supporter
            events
            mock_display_elements = mocker.patch.object(GenericView, "display_elements")
            SupporterController().display_all_events_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_test_display_all_events_of_user_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # test should display customers elements.
        with db_session as session:
            users
            current_user_is_supporter
            mock_display_elements = mocker.patch.object(GenericView, "no_data_message")
            SupporterController().display_all_events_of_user(session=session)
            mock_display_elements.assert_called_once()

    def test_select_event(self, db_session, users, current_user_is_supporter, events, mocker):
        # test should return a good element choosen in list.
        with db_session as session:
            users
            current_user_is_supporter
            events
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=0,
            )
            result = SupporterController().select_event(session=session)
            assert result == events[1]  # event[1] is managed by currentuser.

    def test_select_event_with_no_data(self, db_session, users, current_user_is_supporter, mocker):
        # test should return None.
        with db_session as session:
            users
            current_user_is_supporter
            result = SupporterController().select_event(session=session)
            assert result is None
