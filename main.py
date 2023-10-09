import jwt
from crm.controller.db_controller import Database
from crm.controller.login_controller import LoginController
from crm.controller.user_controller import UserController
from crm.models.sentry import Sentry
from crm.view.generic_view import GenericView


sentry = Sentry().sentry_skd()


def main():
    db = Database()

    while True:
        try:
            db_session = db.create_session()
            with db_session.begin() as session:
                user = LoginController().user_login(session=session)
                LoginController().define_main_user_of_session(session=session, user_connected=user)
                UserController().home_page(session=session)
                session.current_user = None
                session.current_user_department = None
        except (jwt.InvalidTokenError, jwt.InvalidSignatureError, jwt.ExpiredSignatureError, jwt.DecodeError) as msg:
            GenericView().console.print("session expired. Disconned!")
            sentry.capture_exception(msg)
        except KeyboardInterrupt:
            GenericView().console.print("Programme Stopped!")
        except Exception as msg:
            GenericView().console.print("OOoops, an error has occurred, session disconnected")
            sentry.capture_exception(msg)
        finally:
            session.commit()
            session.close()

        if GenericView().ask_comfirmation(message=" quit programme?"):
            break


if __name__ == "__main__":
    main()
