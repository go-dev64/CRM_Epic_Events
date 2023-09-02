# utiliser setup et towdnown
import pytest
from models.users import Manager, Seller, Supporter


class TestLogin:
    def setup(self, mocked_session):
        """
        Initialising the test database and adding data for the test environment.

        Args:
            mocked_session (_type_): Mock of session database.
        """
        self.session = mocked_session
        manager = Manager(
            name="manager", email_address="manager@gmail.com", phone_number="+0335651", password="password"
        )
        seller = Seller(name="seller", email_address="seller@gmail.com", phone_number="+0335651", password="password")
        supporter = Supporter(
            name="supporter", email_address="supporter@gmail.com", phone_number="+0335651", password="password"
        )
        self.session.add_all([manager, seller, supporter])

    def teardown(self):
        """
        Cleaning the mocked database.
        """
        self.session.rollback()

    @pytest.mark.parametrize(
        "email",
        "user_name",
        [
            ("manager@gmail.com", "manager"),
            ("seller@gmail.com", "seller"),
            ("supporter@gmail.com", "supporter"),
        ],
    )
    def test_find_user_with_right_email(email, user_name):
        email_input = email
        user = find_user_with_email(email_input)
        assert user.name == user_name
