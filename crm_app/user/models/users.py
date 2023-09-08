from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from crm_app.user.models.base import Base, intpk, required_name, timestamp
from crm_app.crm.models.customer import Customer, Event, Contract


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

    def authenticated(self, email, password):
        pass

    def __repr__(self):
        return f"User {self.name} - team:{self.department}"


class Supporter(User):
    __tablename__ = "supporter_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    # listes des evenements gerer( one-to-many)
    events: Mapped[list["Event"]] = relationship(back_populates="supporter")

    __mapper_args__ = {"polymorphic_identity": "supporter_table"}

    def update_event(self, event):
        pass


class Manager(User):
    __tablename__ = "manager_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "manager_table"}

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


class Seller(User):
    __tablename__ = "seller_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "seller_table"}

    # relationship
    # listes des clients gerer( one-to-many)
    customers: Mapped[list["Customer"]] = relationship(back_populates="seller_contact")
    # listes des contrats gerer( one-to-many)
    contracts: Mapped[list["Contract"]] = relationship(back_populates="seller")

    def create_customer(self):
        pass

    def update_customer(self, customer):
        pass

    def update_contract(self, contract):
        pass

    def create_event(self):
        pass
