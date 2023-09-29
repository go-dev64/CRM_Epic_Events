from crm.controller.db_controller import Database
from crm.controller.login_controller import LoginController
from crm.controller.user_controller import UserController
from crm.models.utils import Utils


def main():
    db = Database()
    # db.create_tables()
    db_session = db.create_session()
    with db_session as session:
        while True:
            user = LoginController().user_login(session=session)
            session.current_user = user
            current_user_department = Utils().get_type_of_user(user=user)
            session.current_user_department = current_user_department
            UserController().home_page(session=session)
            session.current_user = None
            session.current_user_department = None
            session.commit()
            session.close()


if __name__ == "__main__":
    main()
