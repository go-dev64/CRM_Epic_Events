from crm.models.authentication import Authentication
from crm.view.generic_view import GenericView


class SupporterController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()

    @auth.is_authenticated
    def display_event_of_user(self, session):
        event_list = session.current_user.get_event_of_supporter(session=session)
        return self.generic_view.display_element(event_list)
