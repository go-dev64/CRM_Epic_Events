from datetime import date
from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from crm.models.element_administratif import Event, Contract
from crm.models.base import Base, intpk, required_name, timestamp


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    company: Mapped[Optional[str]] = mapped_column(String(100))
    created_date: Mapped[timestamp]

    updated_date = mapped_column(DateTime)

    events: Mapped[list["Event"]] = relationship(back_populates="customer")

    contracts: Mapped[list["Contract"]] = relationship(back_populates="customer")

    seller_contact_id = mapped_column(ForeignKey("seller_table.id"))
    seller_contact = relationship("Seller", back_populates="customers")

    def set_updated_date(self):
        self.updated_date = date.today()

    def availables_attribue_list(self) -> dict:
        return [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 12}},
            {"attribute_name": "company", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "seller", "parametre": {"type": object}},
        ]

    def __repr__(self) -> str:
        return f"Client: {self.name} - company: {self.company} - contact Epic Event: {self.seller_contact}"
