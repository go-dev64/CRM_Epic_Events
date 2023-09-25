import argon2
import jwt
import os
from dotenv import load_dotenv
from functools import wraps

from sqlalchemy import select
from crm.models.users import User

load_dotenv()


class Authentication:
    def get_user_with_email(self, session, email: str):
        """
        function return User usinfg input email.

        Args:
            email (str): Input email.

        Returns:
            _type_: User and None if fails.
        """
        stmt = select(User).where(User.email_address == email)
        user = session.scalars(stmt).all()
        if len(user) == 1:
            return user[0]
        else:
            return None

    def login(self, session, email: str, input_password: str):
        """
        User login function.
        Return User, None if email invalid and False if password invalid.

        Args:
            email (str]): User email.
            input_password (str]): Password input by user.

        Returns:
            User connected or None if invalid email  and False if invalid pasword.
        """

        user = self.get_user_with_email(session, email=email)
        if user == None:
            return None
        else:
            try:
                ph = argon2.PasswordHasher()
                ph.verify(user.password, input_password)
            except argon2.exceptions.VerifyMismatchError:
                return False
            else:
                return user

    @staticmethod
    def get_token(user):
        """
        Function provide a token to user connected.

        Args:
            user ([User]): User connected after login.

        Returns:
            _type_ : User wiyhin token.
        """
        payload_data = {"sub": user.id, "name": user.name, "department": user.department}
        token = jwt.encode(payload=payload_data, key=os.getenv("TOKEN_KEY"))
        user.token = token
        return user

    @staticmethod
    def decode_token(token: str, token_key: str = os.getenv("TOKEN_KEY")):
        """
        Function to decode token.
        Return a dictionnaire within id, name and department of user.

        Args:
            token (str]): token

        Returns:
            {dict}: dictionnaire within id, name and department of user.
        """
        try:
            headres_token = jwt.get_unverified_header(token)
            token_decoded = jwt.decode(token, key=token_key, algorithms=[headres_token["alg"]])
        except (jwt.InvalidTokenError, jwt.InvalidSignatureError, jwt.ExpiredSignatureError, jwt.DecodeError):
            return None
        else:
            return token_decoded

    @staticmethod
    def is_authenticated(func):
        """
        Function decorator that valides whatever current user is authenticed.

        Args:
            func (_type_): _description_

        Returns:
            _type_: function decorated.
        """

        @wraps(func)
        def validation_token(*args, **kwargs):
            try:
                user = kwargs["session"].current_user

                token_decoded = Authentication.decode_token(token=user.token)
            except AttributeError:
                print("attirubt error")
                return None
            else:
                if token_decoded is not None:
                    value = func(*args, **kwargs)
                    return value
                else:
                    print("token decode eror")
                    return None

        return validation_token
