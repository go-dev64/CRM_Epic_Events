from crm.controller.seller_controller import SellerController
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
    def display_all_events(self, session):
        """The funtion is used to display all events.
        display msg no data if there are no events to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Events"
        title_table = "Table of all Events"
        event_list = Supporter().get_all_events(session=session)
        if len(event_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=event_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_all_events_of_user(self, session):
        """The funtion is used to display all events managed by user.
        display msg no data if there are no events to display.

        Args:
            session (_type_): _description_
        """
        section = "Display Events"
        title_table = "Table of all your Events"
        event_list = Supporter().get_event_of_supporter(session=session)
        if len(event_list) > 0:
            self.generic_view.display_elements(
                session=session,
                section=section,
                elements_list=event_list,
                title_table=title_table,
            )
        else:
            self.generic_view.no_data_message(session=session, section=section, msg=f"No data for {title_table}")

    @auth.is_authenticated
    def display_event(self, session):
        """Function enabling the user to select an action between display all events,
        display his eventd , and back.

        Returns:
            _type_: Return the function executing the action chosen by user.
        """
        choice_list = ["Display all Events", "Display your Events ", "Back to previous menu"]
        while True:
            choice = self.generic_view.select_element_in_menu_view(
                section="Display Events/ Select an action",
                department=session.current_user_department,
                current_user_name=session.current_user,
                list_element=choice_list,
            )
            match choice:
                case 0:
                    self.display_all_events(session=session)
                case 1:
                    self.display_all_events_of_user(session=session)
                case 2:
                    break

    @auth.is_authenticated
    def select_event(self, session) -> Event:
        """The function is used to select a event managed bu current user..

        Returns:
            Event: Event selected.
        """
        section = "Update your Event/Select Event"
        event_list = Supporter().get_event_of_supporter(session=session)
        if len(event_list) > 0:
            event_selected = self.utils._select_element_in_list(
                session=session, section=section, element_list=event_list
            )
            return event_selected
        else:
            return None

    @auth.is_authenticated
    def change_address_of_event(self, session, event_selected: Event):
        """The function is used to change address of event selected.

        Args:
            session (_type_): _description_
            event_selected (Event): Event selected.
        """
        address = SellerController().select_address_of_event(session=session)
        Supporter().update_event(session=session, event=event_selected, attribute_updated="address", new_value=address)

    @auth.is_authenticated
    def change_attribute_of_event(self, session, event_selected: Event, attribute_selected: str):
        """The function is used to update an attribute of event selected.

        Args:
            session (_type_): _description_
            event_selected (Event): Event selected.
            attribute_selected (str): Attribute to be updated of event selected.
        """
        new_value = self.generic_view.get_new_value_of_attribute(
            section=f"New Value of {attribute_selected}",
            department=session.current_user_department,
            current_user=session.current_user.name,
            element=event_selected,
            attribute_selected=attribute_selected,
        )
        Supporter().update_event(
            session=session, event=event_selected, attribute_updated=attribute_selected, new_value=new_value
        )

    @auth.is_authenticated
    def update_element(self, session):
        """the function is used to updated a event.

        Args:
            session (_type_): _description_
        """

        event = self.select_event(session=session)
        if event is not None:
            attribute_selected = self.utils._select_attribut_of_element(
                session=session, section="Update your Event/Select Attribute", element=event
            )
            if attribute_selected in ["contract", "supporter"]:
                self.generic_view.forbidden_acces(session=session, section="Update Event/ forbidden attribut")

            elif attribute_selected == "address":
                self.change_address_of_event(session=session, event_selected=event)
            else:
                self.change_attribute_of_event(
                    session=session, event_selected=event, attribute_selected=attribute_selected
                )
        else:
            self.generic_view.no_data_message(
                session=session,
                section="Upadte Event event",
                msg="There are no availble Event.Update Event is not possible!",
            )
