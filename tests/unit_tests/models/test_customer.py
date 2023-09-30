import pytest
from crm.models.customer import Customer


class TestCustomer:
    def test_availables_attribue_list(self):
        assert Customer().availables_attribue_list() == [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 12}},
            {"attribute_name": "company", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "seller_contact", "parametre": {"type": object}},
        ]

    def test_attribut_to_display(self):
        assert Customer().attribute_to_display() == [
            "name",
            "email_address",
            "phone_number",
            "company",
            "seller_contact",
            "created_date",
            "updated_date",
            "contracts",
            "events",
        ]
