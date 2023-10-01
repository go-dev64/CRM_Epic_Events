from datetime import datetime
import pytest
from crm.controller.supporter_controller import SupporterController


class TestSupportController:
    def test_select_event(self, db_session, events, users, current_user_is_supporter, mocker):
        with db_session as session:
            users
            events
            current_user_is_supporter
            mocker.patch(
                "crm.view.generic_view.GenericView.select_element_in_menu_view",
                return_value=0,
            )
            result = SupporterController().select_event(session=session)
            assert result == events[1]

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
    def test_update_element(
        self, db_session, clients, users, contracts, events, current_user_is_supporter, mocker, attribute, new_value
    ):
        # Test should retrun a event updated.
        with db_session as session:
            users
            contracts
            events
            current_user_is_supporter
            supporter = SupporterController()
            mocker.patch("crm.models.users.Supporter.get_event_of_supporter", retrun_value=[])
            mocker.patch("crm.models.utils.Utils._select_element_in_list", return_value=events[0])
            mocker.patch("crm.models.utils.Utils._select_attribut_of_element", return_value=attribute)
            mocker.patch("crm.view.generic_view.GenericView.get_new_value_of_attribute", return_value=new_value)
            supporter.update_element(session=session)
            assert getattr(events[0], attribute) == new_value
