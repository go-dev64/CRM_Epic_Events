class Event:
    def __init__(self, name, date_start, date_end, address, note, support_contact, customer, contract) -> None:
        self.name = name
        self.customer = customer
        self.contract = contract
        self.date_start = date_start
        self.date_end = date_end
        self.address = address
        self.note = note
        self.support_contact = support_contact
