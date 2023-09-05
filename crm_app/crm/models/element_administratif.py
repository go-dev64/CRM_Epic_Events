from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from crm_app.user.models.base import Base, intpk, required_name, timestamp


class Event(Base):
    __tablename__ = "event_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    date_start = mapped_column(DateTime, nullable=False)
    date_end = mapped_column(DateTime, nullable=False)
    attendees: Mapped[int] = mapped_column()
    note: Mapped[Optional[str]] = mapped_column(String(2048))

    # relationship to customer
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_table.id"))
    customer = relationship("Customer", back_populates="events")
    # relationship to contract
    contract_id: Mapped[int] = mapped_column(ForeignKey("contract_table.id"))
    contract: Mapped["Contract"] = relationship(back_populates="event")
    # relationship to support
    supporter_id = mapped_column(ForeignKey("supporter_table.id"))
    supporter = relationship("Supporter", back_populates="events")

    address_id: Mapped[int] = mapped_column(ForeignKey("address_table.id"))
    address: Mapped["Address"] = relationship(back_populates="event")


class Contract(Base):
    __tablename__ = "contract_table"

    id: Mapped[intpk]
    total_amount: Mapped[int] = mapped_column()
    remaining: Mapped[int] = mapped_column()
    created_date: Mapped[timestamp] = mapped_column()
    signed_contract: Mapped[bool] = mapped_column()

    # relasionship
    event: Mapped["Event"] = relationship(uselist=False, back_populates="contract")

    seller_id: Mapped[int] = mapped_column(ForeignKey("seller_table.id"))
    seller = relationship("Seller", back_populates="contracts")

    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_table.id"))
    customer = relationship("Customer", back_populates="contracts")


class Address(Base):
    __tablename__ = "address_table"

    id: Mapped[intpk]
    number: Mapped[int] = mapped_column()
    street: Mapped[str] = mapped_column(String(500))
    city: Mapped[str] = mapped_column(String(100))
    postal_code: Mapped[int] = mapped_column()
    country: Mapped[str] = mapped_column(String(50))
    note: Mapped[Optional[str]] = mapped_column(String(2048))

    event = relationship("Event", back_populates="address")
    company = relationship("Company", back_populates="address")
