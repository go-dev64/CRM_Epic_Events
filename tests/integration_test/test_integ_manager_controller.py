import pytest
from sqlalchemy import select
from crm.controller.manager_controller import ManagerController
from crm.models.element_administratif import Contract
from crm.models.users import Manager, Seller, Supporter, User


class TestManagerController:
    @pytest.mark.parametrize("department", [(1), (2), (3)])
    def test_create_new_user(self, db_session, users, current_user_is_manager, mocker, department):
        with db_session as session:
            users
            current_user_is_manager
            manager_ctrl = ManagerController()
            user_info = {
                "name": "toto",
                "email_address": "email@fr",
                "phone_number": "+064849",
                "password": "password",
            }
            mocker.patch("crm.view.generic_view.GenericView.select_element_view", return_value=department)
            mocker.patch("crm.view.user_view.UserView.get_user_info_view", return_value=user_info)

            if department == 1:
                new_user = manager_ctrl.create_new_user(session=session)
                list_manager = session.scalars(select(Manager)).all()
                list_user = session.scalars(select(User)).all()
                assert len(list_manager) == 2
                assert len(list_user) == 4

            elif department == 2:
                new_user = manager_ctrl.create_new_user(session=session)
                list_seller = session.scalars(select(Seller)).all()
                list_user = session.scalars(select(User)).all()
                assert len(list_seller) == 2
                assert len(list_user) == 4
            elif department == 3:
                new_user = manager_ctrl.create_new_user(session=session)
                list_supporter = session.scalars(select(Supporter)).all()
                list_user = session.scalars(select(User)).all()
                assert len(list_supporter) == 2
                assert len(list_user) == 4

    def test_create_new_contract(self, db_session, users, clients, contracts, current_user_is_manager, mocker):
        with db_session as session:
            contracts
            current_user_is_manager
            manager_ctrl = ManagerController()
            contract_info = {
                "total_amount": 1000,
                "remaining": 0,
                "signed_contract": True,
                "customer": clients[0],
                "seller": users[1],
            }
            mocker.patch("crm.view.contract_view.ContractView.get_info_contract", return_value=contract_info)
            new_contract = manager_ctrl.create_new_contract(session=session)
            list_contract = session.scalars(select(Contract)).all()
            assert len(list_contract) == 3
