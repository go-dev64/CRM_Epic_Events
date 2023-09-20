from datetime import datetime
import pytest
from sqlalchemy import select
from crm.controller import seller_controller
from crm.controller.manager_controller import ManagerController
from crm.models.users import Manager, Seller, Supporter, User, Event, Customer


class TestSellerController:
    def test_create_new_costumer(self, db_session, clients, current_user_is_seller, mocker):
        with db_session as session:
            clients
            current_user_is_seller
            customer_info = {
                "name": "toto le client",
                "email_address": "email@com",
                "phone_number": "+516184684",
                "company": "une company",
            }
            mocker.patch("crm.view.customer_view.CustomerView.get_info_customer", return_value=customer_info)

            new_customer = seller_controller.SellerController().create_new_customer(session=session)
            list_customer = session.scalars(select(Customer)).all()
            assert len(list_customer) == 3
            assert new_customer.name == customer_info["name"]
            assert new_customer.email_address == customer_info["email_address"]
            assert new_customer.phone_number == customer_info["phone_number"]
            assert new_customer.company == customer_info["company"]
            assert new_customer.seller_contact == session.current_user

    def test_create_new_event(self, db_session, contracts, address, current_user_is_seller, mocker):
        # test should return a new event in event list.
        with db_session as session:
            contract = contracts[0]
            address = address
            current_user = current_user_is_seller
            event_info = {
                "name": "new_event",
                "date_start": datetime.now(),
                "date_end": datetime.now(),
                "attendees": 20,
                "note": "queles notes",
                "contract": contract,
                "supporter": None,
                "address": address,
            }
            mocker.patch("crm.view.event_view.EventView.get_event_info", return_value=event_info)

            new_event = seller_controller.SellerController().create_new_event(session=session)
            list_event = session.scalars(select(Event)).all()
            assert len(list_event) == 1
            assert new_event.name == event_info["name"]
            assert new_event.date_start == datetime
            assert new_event.date_end == datetime
            assert new_event.attendees == event_info["attendees"]
            assert new_event.note == event_info["note"]
            assert new_event.address == address
