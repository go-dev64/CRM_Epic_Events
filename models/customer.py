import datetime
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.users import intpk, required_name, timestamp
from models.element_administratif import Base


class Company(Base):
    __tablename__ = "company_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    phone_number: Mapped[str] = mapped_column(String(10))
    number_of_employee: Mapped[int] = mapped_column()

    address_id: Mapped[int] = mapped_column(ForeignKey("company_table.id"))
    address: Mapped["Company"] = relationship(back_populates="event")

    employees: Mapped[list[int]] = relationship("Customer", back_populates="company")


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(12))
    created_date: Mapped[timestamp]

    updated_date = mapped_column(DateTime)

    company_id: Mapped[int] = mapped_column(ForeignKey("company_table.id"))
    company: Mapped["Company"] = relationship(back_populates="employes")

    events = relationship("Event", back_populates="customer")
    contracts = relationship("Contract", back_populates="customer")

    seller_contact_id = mapped_column(ForeignKey("seller_table.id"))
    seller_contact = relationship("Seller", back_populates="customer")
