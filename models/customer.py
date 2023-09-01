from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from models.base import Base, intpk, required_name, timestamp


class Company(Base):
    __tablename__ = "company_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    number_of_employee: Mapped[int] = mapped_column()

    address_id: Mapped[int] = mapped_column(ForeignKey("address_table.id"))
    address = relationship("Address", back_populates="company")

    employees: Mapped[list[int]] = relationship("Customer", back_populates="company")


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    created_date: Mapped[timestamp]

    updated_date = mapped_column(DateTime)

    company_id: Mapped[int] = mapped_column(ForeignKey("company_table.id"))
    company: Mapped["Company"] = relationship(back_populates="employees")

    events = relationship("Event", back_populates="customer")
    contracts = relationship("Contract", back_populates="customer")

    seller_contact_id = mapped_column(ForeignKey("seller_table.id"), nullable=False)
    seller_contact = relationship("Seller", back_populates="customers")
