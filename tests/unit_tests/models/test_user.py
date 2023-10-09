from sqlalchemy import select
from crm.models.element_administratif import Contract, Event
from crm.models.users import Manager, Seller, Supporter, Address, User
from crm.models.customer import Customer


client = Customer(name="client_1", email_address="clien_1@123.com", phone_number="123456", company="7eme_company")


class TestUser:
    def _count_number_of_element(self, session) -> tuple():
        """the function count number of element in session.

        Args:
            session (_type_): _description_

        Returns:
            tuple(int,int,int,int): number_customer, number_contract, number_event, number_address
        """
        number_contract = len(session.scalars(select(Contract)).all())
        number_customer = len(session.scalars(select(Customer)).all())
        number_event = len(session.scalars(select(Event)).all())
        number_address = len(session.scalars(select(Address)).all())
        return number_customer, number_contract, number_event, number_address

    def _count_number_of_user(self, session) -> tuple:
        """the function count number of users in session.

        Args:
            session (_type_): _description_

        Returns:
            tuple: (number_user, number_manager, number_seller, number_supporter)
        """
        number_manager = len(session.scalars(select(Manager)).all())
        number_seller = len(session.scalars(select(Seller)).all())
        number_supporter = len(session.scalars(select(Supporter)).all())
        number_user = len(session.scalars(select(User)).all())
        return number_user, number_manager, number_seller, number_supporter

    def test_get_all_clients(self, db_session, users, clients):
        # test should return list of clients.
        with db_session as session:
            users
            clients
            result_excepted = self._count_number_of_element(session=session)[0]
            customers_list = User().get_all_customers(session=session)
            assert len(customers_list) == result_excepted

    def test_get_all_contracts(self, db_session, contracts):
        # test should return list of contracts.
        with db_session as session:
            contracts
            result_excepted = self._count_number_of_element(session)[1]
            contract_list = User().get_all_contracts(session=session)
            assert len(contract_list) == result_excepted

    def test_get_all_events(self, db_session, events):
        # test should return list of events.
        with db_session as session:
            events
            result_excepted = self._count_number_of_element(session)[2]
            events_list = User().get_all_events(session=session)

            assert len(events_list) == result_excepted

    def test_get_all_addreses(self, db_session, address):
        # test should return list of address.
        with db_session as session:
            address
            result_excepted = self._count_number_of_element(session)[3]
            events_list = User().get_all_adress(session=session)
            assert len(events_list) == result_excepted

    def test_create_new_address(self, db_session, address):
        # test should return a new address in address list.
        with db_session as session:
            address
            address_info = {
                "number": 12,
                "street": "street",
                "city": "city",
                "postal_code": 45398,
                "country": "france",
                "note": "une note",
            }
            number_addres_before = self._count_number_of_element(session)[3]
            User().create_new_address(session=session, address_info=address_info)
            number_addres = self._count_number_of_element(session)[3]
            assert number_addres == number_addres_before + 1

    def test_attribute_to_display(self):
        assert User().attribute_to_display() == [
            "name",
            "email_address",
            "phone_number",
            "department",
            "created_date",
        ]

    def test_availables_attribue_list(self):
        assert User().availables_attribue_list() == [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 10}},
            {"attribute_name": "password", "parametre": {"type": str, "max": None}},
            {"attribute_name": "department", "parametre": {"type": object, "max": None}},
        ]
