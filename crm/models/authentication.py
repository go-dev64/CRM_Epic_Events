import datetime
import argon2
import jwt
import os
import re
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
        payload_data = {
            "sub": user.id,
            "name": user.name,
            "department": user.department,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=300),
        }
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
        headres_token = jwt.get_unverified_header(token)
        token_decoded = jwt.decode(token, key=token_key, algorithms=[headres_token["alg"]])
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
                session = kwargs["session"]
                user = session.current_user
                Authentication.decode_token(token=user.token)
            except AttributeError:
                return None
            else:
                session.current_user = Authentication.get_token(user)
                session.current_user_department = type(user).__name__
                value = func(*args, **kwargs)
                return value

        return validation_token

    @staticmethod
    def _password_validator(password):
        """
        Function check validity of password.
        Rules:
        1 - Minimum 8 characters.
        2 - The alphabet must be between [a-z]
        3 - At least one alphabet should be of Upper Case [A-Z]
        4 - At least 1 number or digit between [0-9].
        5 - At least 1 character from [ _ or @ or $ ]

        Args:
            password (_type_): password entred by user.

        Returns:
            _type_: True if password respect the Rules and None if it does not.
        """
        flag = 0
        while True:
            if len(password) <= 8:
                flag = -1
                break
            elif not re.search("[a-z]", password):
                flag = -1
                break
            elif not re.search("[A-Z]", password):
                flag = -1
                break
            elif not re.search("[0-9]", password):
                flag = -1
                break
            elif not re.search("[_@$]", password):
                flag = -1
                break
            elif re.search(r"\s", password):
                flag = -1
                break
            else:
                flag = 0
                break

        if flag == -1:
            return None
        else:
            return True
