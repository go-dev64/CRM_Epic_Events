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

    def test_create_new_user(self, db_session):
        with db_session as session:
            current_user = session.scalars(select(Manager)).first()
            new_user = Seller(
                name="new_seller", email_address="manager@gmail.com", phone_number="+0335651", password="passpord"
            )
            current_user.create_new_user(new_user)
            result_excpected = 2
            result = session.scalars(select(Seller)).all()
            assert len(result) == result_excpected
