from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from crm_app.user.models.base import Base, intpk, required_name, timestamp


class Customer(Base):
    __tablename__ = "customer_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    email_address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(12))
    company: Mapped[Optional[str]] = mapped_column(String(100))
    created_date: Mapped[timestamp]

    updated_date = mapped_column(DateTime)

    events = relationship("Event", back_populates="customer")
    contracts = relationship("Contract", back_populates="customer")

    seller_contact_id = mapped_column(ForeignKey("seller_table.id"), nullable=False)
    seller_contact = relationship("Seller", back_populates="customers")
