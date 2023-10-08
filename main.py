from crm.controller.db_controller import Database
from crm.controller.login_controller import LoginController
from crm.controller.user_controller import UserController
from crm.models.exceptions import SessionEnd
from crm.models.sentry import Sentry
from crm.view.generic_view import GenericView


# Sentry().sentry_skd()


def main():
    db = Database()

    db_session = db.create_session()
    try:
        with db_session.begin() as session:
            # db.create_popultaes(session=session)
            LoginController().user_login(session=session)
            UserController().home_page(session=session)
            session.current_user = None
            session.current_user_department = None
    except SessionEnd as msg:
        GenericView().confirmation_msg(session=session, section="disconnect", msg=msg)
    finally:
        session.commit()
        session.close()


if __name__ == "__main__":
    main()
