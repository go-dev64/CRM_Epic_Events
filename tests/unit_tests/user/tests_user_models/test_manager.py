import pytest
from sqlalchemy import select
from crm_app.user.models.users import Manager, Seller, Supporter, User


class TestManager:
    def _create_users(self, session, users):
        # Create users for test.
        session.add_all(users)
        session.commit()

    def _set_current_user(self, session):
        current_user = session.scalars(select(Manager)).first()
        return current_user

    def test_create_new_user(self, db_session, users):
        with db_session as session:
            self._create_users(session, users)
            current_user = session.scalars(select(Manager)).first()
            new_user = {
                "name": "new_seller",
                "email_address": "new_seller@gmail.com",
                "phone_number": "+0335651",
                "password": "passpord",
            }
            new_user = current_user._create_new_user(session, info_user=new_user)
            result_excpected = 4
            new_result = session.scalars(select(User)).all()
            assert len(new_result) == result_excpected

    def test_create_new_user_with_bad_data(self, db_session, users):
        with db_session as session:
            self._create_users(session, users)
            current_user = session.scalars(select(Manager)).first()
            new_user = {
                "name": "new_seller",
                "email_address": "manager@gmail.com",
                "phone_number": "+0335651",
                "password": "passpord",
            }
            new_user = current_user._create_new_user(session, info_user=new_user)
            result_excpected = 3
            new_result = session.scalars(select(User)).all()
            assert len(new_result) == result_excpected
