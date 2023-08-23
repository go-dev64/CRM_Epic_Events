class Customer:
    def __init__(self, name, email_address, phone_number, created_date, updated_date) -> None:
        self.name = name
        self.email_address = email_address
        self.phone_number = phone_number
        self.created_date = created_date
        self.updated_date = updated_date


class Company:
    def __init__(self, company_name, address, phone_number, number_of_employe, siret) -> None:
        self.company_name = company_name
        self.phone_number = phone_number
        self.adress = address
        self.number_of_employe = number_of_employe
        self.siret = siret
