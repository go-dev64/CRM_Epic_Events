# utiliser setup et towdnown
import pytest
from crm_app.user.models.users import Manager, Seller, Supporter
from crm_app.user.models.authentiction import Authentication


class TestLogin:

    """@pytest.mark.parametrize(
        "email",
        "user_name",
        [
            ("manager@gmail.com", "manager"),
            ("seller@gmail.com", "seller"),
            ("supporter@gmail.com", "supporter"),
        ],
    )"""

    def test_find_user_with_right_email(self, db_session, users):
        db_session.add_all(users)
        db_session.commit()
        auth = Authentication(db_session)
        user = auth.find_user_with_email(email="manager@gmail.com")
        print(user)
        assert user.name == "manager"
