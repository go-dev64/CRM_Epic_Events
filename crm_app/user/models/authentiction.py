from sqlalchemy import and_, select
from crm_app.user.models.users import User, Manager, Seller, Supporter


class Authentication:
    def __init__(self, session) -> None:
        self.session = session

    def login(self, email: [str], password: [str]):
        """
        User login function. Return User and None if fails.

        Args:
            email (str]): User email.
            password (str]): Password user

        Returns:
            User connected or None if Fails.
        """

        try:
            with self.session as session:
                stmt = select(User).where(and_(User.email_address == email, User.password == password))
                user = session.scalars(stmt).all()
                if user == None:
                    return None
                return user[0]
        except:
            session.rollback
