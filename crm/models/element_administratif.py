from typing import Optional
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from crm.models.base import Base, intpk, required_name, timestamp


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

    def availables_attribue_list(self) -> dict:
        return [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "date_start", "parametre": {"type": "date", "max": None}},
            {"attribute_name": "date_end", "parametre": {"type": "date", "max": None}},
            {"attribute_name": "address", "parametre": {"type": object, "max": None}},
            {"attribute_name": "attendees", "parametre": {"type": int, "max": None}},
            {"attribute_name": "note", "parametre": {"type": str, "max": 2048}},
            {"attribute_name": "contract", "parametre": {"type": object, "max": None}},
            {"attribute_name": "supporter", "parametre": {"type": object, "max": None}},
        ]

    def attribute_to_display(self) -> list:
        """Function return all attribute availble to be displayed.
        ["name", "customer", "date_start", "date_end", "attendees", "address", "note", "contract", "supporter"]

        Returns:
            list: List of attribute name.
        """
        attribut = [x["attribute_name"] for x in self.availables_attribue_list()]
        attribut.insert(1, "customer")
        return attribut

    def __repr__(self) -> str:
        return f"Event : {self.name} of client :{self.customer.name}"


class Contract(Base):
    __tablename__ = "contract_table"

    id: Mapped[intpk]
    total_amount: Mapped[int] = mapped_column()
    remaining: Mapped[int] = mapped_column()
    created_date: Mapped[timestamp] = mapped_column()
    signed_contract: Mapped[bool] = mapped_column()

    # relasionship
    event: Mapped["Event"] = relationship(uselist=False, back_populates="contract")

    seller_id: Mapped[Optional[int]] = mapped_column(ForeignKey("seller_table.id"))
    seller = relationship("Seller", back_populates="contracts")

    customer_id: Mapped[int] = mapped_column(ForeignKey("customer_table.id"))
    customer = relationship("Customer", back_populates="contracts")

    def availables_attribue_list(self) -> dict:
        return [
            {"attribute_name": "customer", "parametre": "Customer"},
            {"attribute_name": "total_amount", "parametre": {"type": int, "max": None}},
            {"attribute_name": "remaining", "parametre": {"type": int, "max": None}},
            {"attribute_name": "signed_contract", "parametre": {"type": bool, "max": None}},
        ]

    def attribute_to_display(self) -> list:
        """Function return all attribute availble to be displayed.
        list[id, customer, total_amount, remaining, signed_contract, event, seller]

        Returns:
            list: List of attribute name.
        """
        list_attribute = [x["attribute_name"] for x in self.availables_attribue_list()]
        list_attribute.insert(0, "id")
        add_attribute = ["event", "seller"]
        return list_attribute + add_attribute

    def __repr__(self) -> str:
        return f"Contrat N°:{self.id}"


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

    def availables_attribue_list(self) -> dict:
        return [
            {"attribute_name": "number", "parametre": {"type": int, "max": None}},
            {"attribute_name": "street", "parametre": {"type": str, "max": 500}},
            {"attribute_name": "city", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "postal_code", "parametre": {"type": int, "max": None}},
            {"attribute_name": "country", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "note", "parametre": {"type": str, "max": 2048}},
        ]

    def attribute_to_display(self) -> list:
        """Function return all attribute availble to be displayed.
                [number, street, city,postal_code,country, note]
        [        Returns:
                    list: List of attribute name.
        """
        return [x["attribute_name"] for x in self.availables_attribue_list()]

    def __repr__(self) -> str:
        return f"{self.number}, street:{self.street} of {self.city}"
