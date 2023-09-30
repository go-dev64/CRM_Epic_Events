from datetime import datetime
import pytest

from crm.models.users import Supporter


class TestSupporter:
    def test_get_event_of_supporter(self, db_session, events, current_user_is_supporter):
        # test should return events list without supporter.

        with db_session as session:
            events
            current_user = current_user_is_supporter
            event_list_of_user = current_user.get_event_of_supporter(session=session)
            result_excepted = 1
            assert len(event_list_of_user) == result_excepted

    @pytest.mark.parametrize(
        "attribute_updated, new_value",
        [
            ("name", "toto"),
            ("date_start", datetime.now()),
            ("date_end", datetime.now()),
            ("attendees", 50),
            ("notes", "un notes"),
        ],
    )
    def test_update_event(self, db_session, events, current_user_is_supporter, attribute_updated, new_value):
        # Test should return the updated event.
        with db_session as session:
            event = events[0]
            current_user = current_user_is_supporter
            current_user.update_event(
                session=session, event=event, attribute_updated=attribute_updated, new_value=new_value
            )
            assert getattr(event, attribute_updated) == new_value

    def test_update_address_event(self, db_session, events, current_user_is_supporter, address):
        # Test should return the updated event.
        with db_session as session:
            event = events[0]
            address = address
            current_user = current_user_is_supporter
            current_user.update_event(session=session, event=event, attribute_updated="address", new_value=address)
            assert getattr(event, "address") == address

    @pytest.mark.parametrize(
        "attribute_updated, new_value",
        [
            ("customer_id", 1),
            ("customer", "datetime.now()"),
            ("contract_id", datetime.now()),
            ("contract", 50),
            ("supporter_id", "un notes"),
            ("supporter", "un notes"),
        ],
    )
    def test_update_event_with_forbidden_attribute(
        self, db_session, events, current_user_is_supporter, attribute_updated, new_value
    ):
        # Test should return the updated event.
        with db_session as session:
            event = events[0]
            current_user = current_user_is_supporter
            current_user.update_event(
                session=session, event=event, attribute_updated=attribute_updated, new_value=new_value
            )
            assert getattr(event, attribute_updated) != new_value

    def test_attribute_to_display(self):
        assert Supporter().attribute_to_display() == [
            {"attribute_name": "name"},
            {"attribute_name": "email_address"},
            {"attribute_name": "phone_number"},
            {"attribute_name": "created_date"},
            {"attribute_name": "department"},
            {"attribute_name": "events"},
        ]
