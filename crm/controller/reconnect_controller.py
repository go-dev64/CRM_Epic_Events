import time
from crm.controller.login_controller import LoginController
from crm.models.exceptions import EmailError, PasswordError, SessionEnd
from crm.view.login_view import LoginView


class ReconnectingUser:
    def __init__(self) -> None:
        self.login = LoginController()
        self.login_view = LoginView()

    def reconnect_user(self, session, user_expired):
        """The function is used to asking a reconnection to user after token expiration:

        Args:
            session (_type_): _description_
        """
        while True:
            user = self.login.user_login(session=session)
            if user.id == user_expired.id:
                break

        self.login_view.authentication_ok()
        time.sleep(2)
        self.login.define_main_user_of_session(session=session, user_connected=user)

    def reconneting_choice(self, session, user_expired):
        choice_list = [f"Reconnect Session of {user_expired}", "Close Session"]
        choice = self.login_view.generic.select_element_in_menu_view(
            department=user_expired.department,
            current_user=user_expired,
            section="Expired Session",
            list_element=choice_list,
        )
        match choice:
            case 0:
                self.reconnect_user(session=session, user_expired=user_expired)
            case 1:
                raise SessionEnd()
