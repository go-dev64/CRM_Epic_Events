from sqlalchemy import or_, select, or_, text
from crm_app.user.models.users import User, Manager, Seller, Supporter


class Authentication:
    def __init__(self, session) -> None:
        self.session = session

    def find_user_with_email(self, email):
        with self.session as session:
            try:
                stmt = select(User).where(User.email_address == email)

                user = session.scalars(stmt).all()
                for i in user:
                    print(i)
                if user == []:
                    raise ValueError
            except ValueError:
                return None
            else:
                return user[0]
