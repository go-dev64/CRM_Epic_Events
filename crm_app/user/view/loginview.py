# View module of user login.


class LoginView:
    def __init__(self) -> None:
        pass

    def get_user_email_and_password(self, msg=""):
        print(
            "===== Welcome to EPIC EVENTS =====n\
            Please enter your email and password to log in"
        )
        try:
            print(msg)
            email = str(input("Your email: ")).lower
            password = input("Your Password: ")
        except ValueError:
            msg = "Le email doit etre une chaine de caractère"

        else:
            return email, password
