import pytest
from sqlalchemy import select
from crm.controller import seller_controller
from crm.controller.manager_controller import ManagerController
from crm.models.customer import Customer
from crm.models.element_administratif import Contract
from crm.models.users import Manager, Seller, Supporter, User


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
