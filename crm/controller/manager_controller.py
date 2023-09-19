from crm.models.authentication import Authentication


class ManagerController:
    auth = Authentication()

    def __init__(self) -> None:
        self.manager_view = ViewManager()

    def create(self, session)