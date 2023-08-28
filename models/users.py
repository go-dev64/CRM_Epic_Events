import datetime

from typing_extensions import Annotated
from sqlalchemy import DateTime, Integer, ForeignKey, String
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


intpk = Annotated[int, mapped_column(Integer(), primary_key=True, autoincrement=True)]
required_name = Annotated[str, mapped_column(String(50), nullable=False)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class User:
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(10))
    created_date: Mapped[timestamp]
    password: Mapped[str] = mapped_column(String)


class Supporter(Base, User):
    __tablename__ = "supporter_table"

    id: Mapped[intpk]
    department: Mapped[str] = mapped_column(String(), default="Support")

    # listes des evenements gerer( one-to-many)
    events = relationship("Event", back_populates="supporter")

    def update_event(self, event):
        pass

    def __repr__(self):
        return f"User {self.name} - team:{self.department}"


class Manager(Base, User):
    __tablename__ = "manager_table"

    id: Mapped[intpk]
    department: Mapped[str] = mapped_column(String(), default="Management")

    def create_colaborator(self):
        pass

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

    def __repr__(self):
        return f"User {self.name} - team:{self.department}"


class Seller(Base, User):
    __tablename__ = "seller_table"

    id: Mapped[intpk]
    department: Mapped[str] = mapped_column(String(), default="Sales")

    # relationship
    # listes des clients gerer( one-to-many)
    customers = relationship("Customer", back_populates="customer_contact")
    # listes des contrats gerer( one-to-many)
    contracts = relationship("Contract", back_populates="contrat_manager")

    def create_customer(self):
        pass

    def update_customer(self, customer):
        pass

    def update_contract(self, contract):
        pass

    def create_event(self):
        pass

    def __repr__(self):
        return f"User {self.name} - team:{self.department}"
