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
    def select_event(self, session) -> Event:
        """The function is used to select a event managed bu current user..

        Returns:
            Event: Event selected.
        """
        event_list = Supporter().get_event_of_supporter(session=session)
        event_selected = self.utils._select_element_in_list(
            session=session, section="Update your Event/Select Event", element_list=event_list
        )
        return event_selected

    @auth.is_authenticated
    def update_element(self, session):
        """the function is used to updated a event.

        Args:
            session (_type_): _description_
        """
        event = self.select_event(session=session)
        attribute_selected = self.utils._select_attribut_of_element(
            session=session, section="Update your Event/Select Attribute", element=event
        )
        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=event,
            attribute_selected=attribute_selected,
        )
        Supporter().update_event(
            session=session, event=event, attribute_updated=attribute_selected, new_value=new_value
        )
