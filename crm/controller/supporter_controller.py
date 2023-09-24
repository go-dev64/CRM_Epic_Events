from crm.models.authentication import Authentication
from crm.models.utils import Utils
from crm.view.generic_view import GenericView


class SupporterController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.utils = Utils()

    @auth.is_authenticated
    def display_event_of_user(self, session):
        event_list = session.current_user.get_event_of_supporter(session=session)
        return self.generic_view.display_element(event_list)

    @auth.is_authenticated
    def update_element(self, session):
        """
        Function update event of user's.
        """
        events_list = session.current_user.get_event_of_supporter(session=session)
        event = self.utils._select_element_in_list(element_list=events_list)
        attribut_to_be_updated = self.utils._select_attribut_of_element(element=event)
        new_value = self.utils._get_new_value_of_attribut(element=event, attribute_to_updated=attribut_to_be_updated)
        session.current_user.update_event(
            session=session, event=event, attribute_updated=attribut_to_be_updated, new_value=new_value
        )
