class User:
    def __init__(self, name, email_address, phone_number):
        self.name = name
        self.email_address = email_address
        self.phone_number = phone_number
        self.date_created = ""


class Suppporter:
    department = "Support"

    def __init__(self, user, role) -> None:
        self.user = user
        self.role = role
        self.list_of_events = []

    def update_event(self, event):
        pass


class Manager:
    department = "Management"

    def __init__(self, user, role) -> None:
        self.user = user
        self.role = role

    def create_colaborator(self):
        pass

    def update_colaborator(self, colaborator):
        pass

    def delete_colaborator(self, colaborator):
        pass

    def create_contract(self):
        pass

    def update_contract(self, contract):
        pass

    def update_event(self, event):
        pass


class Seller:
    department = "Sales"

    def __init__(self, user, role) -> None:
        self.user = user
        self.role = role

    def create_customer(self):
        pass

    def update_customer(self, customer):
        pass

    def update_contract(self, contract):
        pass

    def create_event(self):
        pass
