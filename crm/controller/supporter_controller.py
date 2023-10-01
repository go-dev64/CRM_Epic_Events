from crm.models.authentication import Authentication
from crm.models.element_administratif import Event
from crm.models.users import Supporter
from crm.models.utils import Utils
from crm.view.generic_view import GenericView


class SupporterController:
    auth = Authentication()

    def __init__(self) -> None:
        self.generic_view = GenericView()
        self.utils = Utils()

    @auth.is_authenticated
    def display_event(self, session):
        """Function enabling the user to select an action between display all events,
        display his eventd , and back.

        Returns:
            _type_: Return the function executing the action chosen by user.
        """
        choice_list = ["Display all Events", "Display your Events ", "Back to previous menu"]
        attributes_displayed = Event().availables_attribue_list()
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Display Events/ Select an action",
                department=session.current_user_department,
                current_user_name=session.current_user,
                list_element=choice_list,
            )
            match choice:
                case 0:
                    events_list = Supporter().get_all_events(session=session)
                    return self.generic_view.display_elements(
                        session=session,
                        section="Display Events",
                        title_table="All Event",
                        elements_list=events_list,
                        attributes=attributes_displayed,
                    )
                case 1:
                    events_of_supporter = Supporter().get_event_of_supporter(session=session)
                    return self.generic_view.display_elements(
                        session=session,
                        section="Display Events",
                        title_table="Event without Supporter",
                        elements_list=events_of_supporter,
                        attributes=attributes_displayed,
                    )
                case 2:
                    break

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
