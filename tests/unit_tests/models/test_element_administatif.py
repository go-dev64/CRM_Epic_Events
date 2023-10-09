from crm.models.element_administratif import Address, Contract, Event


class TestElementAdministratif:
    def test_event_attribute_to_display(self):
        assert Event().attribute_to_display() == [
            "name",
            "customer",
            "date_start",
            "date_end",
            "address",
            "attendees",
            "note",
            "contract",
            "supporter",
        ]

    def test_event_availables_attribue_list(self):
        assert Event().availables_attribue_list() == [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "date_start", "parametre": {"type": "date", "max": None}},
            {"attribute_name": "date_end", "parametre": {"type": "date", "max": None}},
            {"attribute_name": "address", "parametre": {"type": object, "max": None}},
            {"attribute_name": "attendees", "parametre": {"type": int, "max": None}},
            {"attribute_name": "note", "parametre": {"type": str, "max": 2048}},
            {"attribute_name": "contract", "parametre": {"type": object, "max": None}},
            {"attribute_name": "supporter", "parametre": {"type": object, "max": None}},
        ]

    def test_contract_availables_attribue_list(self):
        assert Contract().availables_attribue_list() == [
            {"attribute_name": "customer", "parametre": "Customer"},
            {"attribute_name": "total_amount", "parametre": {"type": int, "max": None}},
            {"attribute_name": "remaining", "parametre": {"type": int, "max": None}},
            {"attribute_name": "signed_contract", "parametre": {"type": bool, "max": None}},
        ]

    def test_contract_attribute_to_display(self):
        assert Contract().attribute_to_display() == [
            "id",
            "customer",
            "total_amount",
            "remaining",
            "signed_contract",
            "event",
            "seller",
        ]

    def test_address_availables_attribue_list(self):
        assert Address().availables_attribue_list() == [
            {"attribute_name": "number", "parametre": {"type": int, "max": None}},
            {"attribute_name": "street", "parametre": {"type": str, "max": 500}},
            {"attribute_name": "city", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "postal_code", "parametre": {"type": int, "max": None}},
            {"attribute_name": "country", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "note", "parametre": {"type": str, "max": 2048}},
        ]

    def test_address_attribute_to_display(self):
        assert Address().attribute_to_display() == [
            "number",
            "street",
            "city",
            "postal_code",
            "country",
            "note",
        ]
