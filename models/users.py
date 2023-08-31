from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.base import Base, intpk, required_name, timestamp


class User:
    id: Mapped[intpk]
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone_number: Mapped[Optional[str]] = mapped_column(String(10))
    created_date: Mapped[timestamp]
    password: Mapped[str] = mapped_column()
    department: Mapped[str] = mapped_column()

    def __init__(self, name, email, phone, password) -> None:
        self.name = name
        self.email_address = email
        self.phone_number = phone
        self.password = password

    def authenticated(self, email, password):
        pass

    def __repr__(self):
        return f"User {self.name} - team:{self.department}"


class Supporter(Base, User):
    __tablename__ = "supporter_table"

    department = "Support"

    # listes des evenements gerer( one-to-many)
    events = relationship("Event", back_populates="supporter")

    def update_event(self, event):
        pass


class Manager(Base, User):
    __tablename__ = "manager_table"

    department = "Manage"

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


class Seller(Base, User):
    __tablename__ = "seller_table"

    # relationship
    # listes des clients gerer( one-to-many)
    customers = relationship("Customer", back_populates="customer_contact")
    # listes des contrats gerer( one-to-many)
    contracts = relationship("Contract", back_populates="contrat_manager")

    department = "Sales"

    def create_customer(self):
        pass

    def update_customer(self, customer):
        pass

    def update_contract(self, contract):
        pass

    def create_event(self):
        pass
