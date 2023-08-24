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


class Contract:
    def __init__(self, total_amount, remaining) -> None:
        self.total_amount = total_amount
        self.remaining = remaining
        self.signed_contract = False


class Address:
    def __init__(self, numero, street, city, postal_code, conntry, details) -> None:
        self.numero = numero
        self.street = street
        self.city = city
        self.postal_code = postal_code
        self.country = conntry
        self.details = details
