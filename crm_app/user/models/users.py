import argon2
import jwt
import os

from dotenv import load_dotenv
from functools import wraps
from sqlalchemy import ForeignKey, String, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional

from crm_app.user.models.base import Base, intpk, required_name, timestamp
from crm_app.crm.models.customer import Customer, Event, Contract

load_dotenv()


class Authentication:
    def __init__(self) -> None:
        self.ph = argon2.PasswordHasher()

    def get_user_with_email(self, session, email: [str]):
        """
        function return User usinfg input email.

        Args:
            email (str]): Input email.

        Returns:
            _type_: User and None if fails.
        """
        stmt = select(User).where(User.email_address == email)
        user = session.scalars(stmt).all()
        if len(user) == 1:
            return user[0]
        else:
            return None

    def login(self, db_session, email: [str], input_password: [str]):
        """
        User login function.
        Return User, None if email invalid and False if password invalid.

        Args:
            email (str]): User email.
            input_password (str]): Password input by user.

        Returns:
            User connected or None if invalid email  and False if invalid pasword.
        """

        user = self.get_user_with_email(db_session, email=email)
        if user == None:
            return None
        else:
            try:
                self.ph.verify(user.password, input_password)
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
    def decode_token(token: [str], token_key: [str] = os.getenv("TOKEN_KEY")):
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


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(10))
    created_date: Mapped[timestamp]
    password: Mapped[str]
    department: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "user_table",
        "polymorphic_on": "department",
    }

    @Authentication.is_authenticated
    def get_all_customers(self, session):
        # Function return all Custumers.
        customers = session.scalars(select(Customer)).all()
        return customers

    @Authentication.is_authenticated
    def get_all_contracts(self, session):
        # Function return all Contracts.
        contracts = session.scalars(select(Contract)).all()
        return contracts

    @Authentication.is_authenticated
    def get_all_events(self, session):
        # Function return all Events.
        events = session.scalars(select(Event)).all()
        return events

    def __repr__(self):
        return f"User {self.name} - team:{self.department}"


class Supporter(User):
    __tablename__ = "supporter_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    # listes des evenements gerer( one-to-many)
    events: Mapped[list["Event"]] = relationship(back_populates="supporter")

    __mapper_args__ = {"polymorphic_identity": "supporter_table"}

    @Authentication.is_authenticated
    def get_event_of_supporter(self, session):
        # Function return all contracts of user.
        contracts_list = session.scalars(select(Event).where(Event.supporter == session.current_user)).all()
        return contracts_list

    def update_event(self, event):
        pass


class Manager(User):
    __tablename__ = "manager_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "manager_table"}

    @Authentication.is_authenticated
    def get_all_users(self, session):
        # Function return all User.
        users = session.scalars(select(User)).all()
        return users

    @Authentication.is_authenticated
    def get_all_event_without_support(self, session):
        # Function return all evant without supporter.
        event_without_supporter = session.scalars(select(Event).where(Event.supporter == None)).all()
        return event_without_supporter

    @Authentication.is_authenticated
    def create_new_manager(self, session, user_info: dict) -> None:
        """
        Function add a new Manager to database.

        Args:
            session (_type_): database session
            user_info (dict): user info.
        """
        try:
            new_manager = Manager(
                name=user_info["name"],
                email_address=user_info["email_address"],
                phone_number=user_info["phone_number"],
                password=user_info["password"],
            )
            session.add(new_manager)
        except (KeyError, ValueError):
            return None
        else:
            session.commit()
            return new_manager

    @Authentication.is_authenticated
    def create_new_seller(self, session, user_info: dict) -> None:
        """
        Function add a new Seller to database.

        Args:
            session (_type_): database session
            user_info (dict): user info.
        """
        try:
            new_seller = Seller(
                name=user_info["name"],
                email_address=user_info["email_address"],
                phone_number=user_info["phone_number"],
                password=user_info["password"],
            )
            session.add(new_seller)
        except (KeyError, ValueError):
            return None
        else:
            session.commit()
            return new_seller

    @Authentication.is_authenticated
    def create_new_supporter(self, session, user_info: dict) -> None:
        """
        Function add a new Supporter to database.

        Args:
            session (_type_): database session
            user_info (dict): user info.
        """
        try:
            new_supporter = Supporter(
                name=user_info["name"],
                email_address=user_info["email_address"],
                phone_number=user_info["phone_number"],
                password=user_info["password"],
            )
            session.add(new_supporter)
        except (KeyError, ValueError):
            return None
        else:
            session.commit()
            return new_supporter

    @Authentication.is_authenticated
    def create_new_contract(self, session, contract_info: dict) -> None:
        """
        Function add a new contract to database.

        Args:
            session (_type_): database session
            contract (dict): contract info.
        """
        try:
            contract = Contract(
                total_amount=contract_info["total_amount"],
                remaining=contract_info["remaining"],
                signed_contract=contract_info["signed_contract"],
                customer=contract_info["customer"],
            )
            session.add(contract)
            contract.seller = contract_info["customer"].seller_contact

        except (KeyError, ValueError) as exc:
            print(exc)
            return None
        else:
            session.commit()
            return contract

    def update_colaborator(self, colaborator):
        pass

    def delete_colaborator(self, colaborator):
        pass

    def create_contract(self):
        pass

    def update_contract(self, contract):
        pass

    def update_event(self, event):
        pass


class Seller(User):
    __tablename__ = "seller_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "seller_table"}

    # relationship
    # listes des clients gerer( one-to-many)
    customers: Mapped[list["Customer"]] = relationship(back_populates="seller_contact")
    # listes des contrats gerer( one-to-many)
    contracts: Mapped[list["Contract"]] = relationship(back_populates="seller")

    @Authentication.is_authenticated
    def get_all_clients_of_user(self, session):
        # Function return all clients of user.
        customers_list = session.scalars(select(Customer).where(Customer.seller_contact == session.current_user)).all()
        return customers_list

    @Authentication.is_authenticated
    def get_all_contracts_of_user(self, session):
        # Function return all contracts of user.
        contracts_list = session.scalars(select(Contract).where(Contract.seller == session.current_user)).all()
        return contracts_list

    @Authentication.is_authenticated
    def get_unsigned_contracts(self, session):
        # Function return all unsigned contracts.
        unsigned_contracts_list = session.scalars(select(Contract).where(Contract.signed_contract == False)).all()
        return unsigned_contracts_list

    @Authentication.is_authenticated
    def get_unpayed_contracts(self, session):
        # Function return all unpayed contracts.
        unpayed_contracts_list = session.scalars(select(Contract).where(Contract.remaining > 0)).all()
        return unpayed_contracts_list

    def create_new_customer(self, session, customer_info):
        try:
            new_customer = Customer(
                name=customer_info["name"],
                email_address=customer_info["email_address"],
                phone_number=customer_info["phone_number"],
                company=customer_info["company"],
                seller_contact=session.current_user,
            )
            session.add(new_customer)
        except (KeyError, ValueError) as exc:
            print(exc)
            return None
        else:
            session.commit()
            return new_customer

    def update_customer(self, customer):
        pass

    def update_contract(self, contract):
        pass

    def create_event(self):
        pass
