from crm.controller.db_controller import Database
from crm.controller.login_controller import LoginController


def main():
    db = Database()
    db.create_tables()
    db_session = db.create_session()
    with db_session as session:
        while True:
            user = LoginController().user_login(session=session)
            session.current_user = user
            LoginController().redirect_user_home_page(session=session)


if __name__ == "__main__":
    main()
