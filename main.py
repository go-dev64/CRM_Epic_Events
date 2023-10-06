import os
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from dotenv import load_dotenv
from crm.controller.db_controller import Database
from crm.controller.login_controller import LoginController
from crm.controller.user_controller import UserController
from crm.models.utils import Utils


load_dotenv()

sentry_sdk.init(
    dsn=os.getenv("DNS_SENTRY"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    integrations=[
        LoggingIntegration(
            level=logging.INFO,  # Capture info and above as breadcrumbs
            event_level=logging.ERROR,  # Send errors as events
        ),
    ],
)


def main():
    db = Database()
    # db.create_tables()
    db_session = db.create_session()
    with db_session.begin() as session:
        # db.create_popultaes(session=session)
        user = LoginController().user_login(session=session)
        session.current_user = user
        current_user_department = Utils().get_type_of_user(user=user)
        session.current_user_department = current_user_department
        foo = UserController().home_page(session=session)
        session.current_user = None
        session.current_user_department = None
        session.commit()
        session.close()


if __name__ == "__main__":
    main()
