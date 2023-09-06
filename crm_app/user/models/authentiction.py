import argon2
from sqlalchemy import and_, select
from crm_app.user.models.users import User, Manager, Seller, Supporter


class Authentication:
    def __init__(self) -> None:
        self.ph = argon2.PasswordHasher()

    def get_user_with_email(self, session, email: [str]):
        """
        function return User usinfg input email.

        Args:
            email (str]): Input email.

        Returns:
            _type_: User and None if fails.
        """
        stmt = select(User).where(User.email_address == email)
        user = session.scalars(stmt).all()
        if len(user) == 1:
            return user[0]
        else:
            return None

    def login(self, db_session, email: [str], input_password: [str]):
        """
        User login function.
        Return User, None if email invalid and False if password invalid.

        Args:
            email (str]): User email.
            input_password (str]): Password input by user.

        Returns:
            User connected or None if invalid email  and False if invalid pasword.
        """

        user = self.get_user_with_email(db_session, email=email)
        if user == None:
            return None
        else:
            try:
                self.ph.verify(user.password, input_password)
            except argon2.exceptions.VerifyMismatchError:
                return False
            else:
                return user
