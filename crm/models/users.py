from sqlalchemy import ForeignKey, String, select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional

from crm.models.base import Base, intpk, required_name, timestamp
from crm.models.customer import Customer, Event, Contract
from crm.models.element_administratif import Address
from crm.models.sentry import Sentry

logger = Sentry().logger()


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

    def get_all_customers(self, session) -> list[Customer]:
        """The function return all customers in list."""

        customers = session.scalars(select(Customer)).all()
        return customers

    def get_all_contracts(self, session) -> list[Contract]:
        """The function return all contracts in list."""

        contracts = session.scalars(select(Contract)).all()
        return contracts

    def get_all_events(self, session) -> list[Event]:
        """Function return all events in list"""

        events = session.scalars(select(Event)).all()
        return events

    def get_all_adress(self, session) -> list[Address]:
        """The function return all addresses in list."""

        addresses = session.scalars(select(Address)).all()
        return addresses

    def create_new_address(self, session, address_info: dict):
        """Function add a new Address.

        Args:
            session (_type_): database session
            user_info (dict): Address info.
        """
        try:
            new_address = Address(
                number=address_info["number"],
                street=address_info["street"],
                city=address_info["city"],
                postal_code=address_info["postal_code"],
                country=address_info["country"],
                note=address_info["note"],
            )
            session.add(new_address)

        except (KeyError, ValueError):
            return None
        else:
            return new_address

    def __repr__(self):
        return f"User {self.name}"

    def availables_attribue_list(self) -> list[dict]:
        """Fuction return a list od dict of attribut availables for creation and update user.

        Returns:
            list[dict]: exemeple:[
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            ]
        """
        return [
            {"attribute_name": "name", "parametre": {"type": str, "max": 50}},
            {"attribute_name": "email_address", "parametre": {"type": str, "max": 100}},
            {"attribute_name": "phone_number", "parametre": {"type": str, "max": 10}},
            {"attribute_name": "password", "parametre": {"type": str, "max": None}},
            {"attribute_name": "department", "parametre": {"type": object, "max": None}},
        ]

    def attribute_to_display(self) -> list:
        """Function return all attribute availble to be displayed(reading).

        Returns:
            list: List  of attribute name.
        """
        attribute_list = [
            x["attribute_name"] for x in self.availables_attribue_list() if x["attribute_name"] != "password"
        ]
        add_attribute = ["created_date"]
        return attribute_list + add_attribute


class Supporter(User):
    __tablename__ = "supporter_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"), primary_key=True)

    # listes des evenements gerer( one-to-many)
    events: Mapped[list["Event"]] = relationship(back_populates="supporter")

    __mapper_args__ = {"polymorphic_identity": "supporter_table"}

    def attribute_to_display(self) -> list:
        """Function return all attribute available to be displayed(reading)."""
        list_attributes = super().attribute_to_display()
        add_attributes = ["events"]
        return list_attributes + add_attributes

    def get_event_of_supporter(self, session) -> list:
        # Function return all contracts of user.
        contracts_list = session.scalars(select(Event).where(Event.supporter == session.current_user)).all()
        return contracts_list

    def update_event(self, session, event, attribute_updated, new_value) -> None:
        """
        Function updates event.
        If Attribute to be updated in forbidden attribute , the function pass.

        Args:
            session (_type_): _description_
            event (Event class): Instance Event class to be updated.
            attribute_updated (str): Attribute to be updated.
            new_value (_type_): New value of attribute to be updated.
        """
        forbidden_attribute = [
            "customer_id",
            "customer",
            "contract_id",
            "contract",
            "supporter_id",
            "supporter",
        ]
        if attribute_updated not in forbidden_attribute:
            setattr(event, attribute_updated, new_value)


class Manager(User):
    __tablename__ = "manager_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "manager_table"}

    def get_all_users(self, session) -> list[User]:
        """Function return all collaborator.

        Args:
            session (_type_): _description_

        Returns:
            list[User]: List of all collaboraotor.
        """
        users = session.scalars(select(User)).all()
        return users

    def get_all_supporter(self, session) -> list[Supporter]:
        """Function returns all Supporter.
        Args:
            session (_type_): actual Session.
        Returns:
            list[Supporter]: list of Suppotrer.
        """
        return session.scalars(select(Supporter)).all()

    def get_all_event_without_support(self, session) -> list[Event]:
        """Function return all event without supporter.
        Args:
            session (_type_):  actual Session
        Returns:
            list[Event]: Event list without Supporter.
        """
        event_without_supporter = session.scalars(select(Event).where(Event.supporter == None)).all()  # noqa
        return event_without_supporter

    def get_customer_without_seller(self, session):
        customers_list = session.scalars(select(Customer).where(Customer.seller_contact == None)).all()  # noqa
        return customers_list

    def create_new_manager(self, session, user_info: dict) -> "Manager":
        """Function add a new Manager to database.

        Args:
            session (_type_): database session
            user_info (dict): user info.

        Return Manager created.
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
            logger.info(f"Creating a new Manager: {new_manager.name}")
            return new_manager

    def create_new_seller(self, session, user_info: dict):
        """Function add a new Seller to database.

        Args:
            session (_type_): database session
            user_info (dict): user info.

        Retrun Seller created.
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
            logger.info(f"Creating a new Seller: {new_seller.name}")
            return new_seller

    def create_new_supporter(self, session, user_info: dict) -> Supporter:
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
            logger.info(f"Creating a new Supporter: {new_supporter.name}")
            return new_supporter

    def create_new_contract(self, session, contract_info: dict) -> Contract:
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
            if contract.signed_contract == True:  # noqa
                logger.info(f"{contract} has been signed.")
            return contract

    def update_user(self, collaborator, update_attribute: str, new_value) -> None:
        """
        This function update a attribut user.

        Args:
            session (_type_): _description_
            colablorator (_type_): a user , Manager, Seller or Supporter.
            update_attribute (str): This attribut should be name or emmail_address or phone_number or password.
            new_value (_type_): new value of update attribute.
        """
        setattr(collaborator, update_attribute, new_value)
        logger.info(f"The {update_attribute} of {collaborator} has been updated to {new_value}")

    def change_user_department(self, session, collaborator, new_department: str):
        """
        This function switch user of department.
        First, it obtaints informations about the user, then deletes the user, and creates a new user,
        with the recovered informations, in the new department.

        Args:
            session (_type_): _description_
            collaborator (_type_): User to move of department.
            new_department (str): new_department : Manager, Seller or Supporter.

        Returns:
            _type_: a user with a class of new department.
        """
        user_info = {
            "name": collaborator.name,
            "email_address": collaborator.email_address,
            "phone_number": collaborator.phone_number,
            "password": collaborator.password,
        }
        self.delete_collaborator(session=session, collaborator_has_delete=collaborator)
        logger.info(f"The {collaborator} has been delete and re-create in new department")
        match new_department:
            case "Manager":
                return self.create_new_manager(session=session, user_info=user_info)
            case "Seller":
                return self.create_new_seller(session=session, user_info=user_info)
            case "Supporter":
                return self.create_new_supporter(session=session, user_info=user_info)

    def update_contract(self, contract: Contract, attribute_update: str, new_value) -> None:
        """
        Function update a attribute of contract.
        If attribute_uptade  is "customer",  the contract's seller attribut will be updated
        to match the customer's seller.

        Args:
            session (_type_): _description_
            contract (_type_): Contract to be updated.
            attribute_update (str): Attribute to be updated.
            new_value (_type_): New value of attribute to be updated.
        """
        if attribute_update == "customer":
            seller = new_value.seller_contact
            setattr(contract, "seller", seller)

        setattr(contract, attribute_update, new_value)
        if attribute_update == "signed_contract":
            logger.info(f"{contract} has been signed!")

    def update_seller_contact_of_customer(self, customer: Customer, new_seller):
        """
        Function update a seller_contact attribute.
        the function will also update the seller attribute of all the customer's contracts.

        Args:
            session (_type_): _description_
            customer (Customer): Instance Customer class to be updated.
            new_seller (_type_): New seller of Instance Customer class.
        """

        setattr(customer, "seller_contact", new_seller)
        for contract in customer.contracts:
            setattr(contract, "seller", customer.seller_contact)

    def change_supporter_of_event(self, session, event: Event, new_supporter: Supporter) -> None:
        """
        Function updates a event supporter.

        Args:
            session (_type_): _description_
            event (class Event): Event to be updated.
            new_supporter (class Supporter): New Supporter od event
        """
        setattr(event, "supporter", new_supporter)

    def delete_collaborator(self, session, collaborator_has_delete: User) -> None:
        session.delete(collaborator_has_delete)
        session.scalars(select(User).where(User.id == collaborator_has_delete.id))
        logger.info(f"The {collaborator_has_delete} has been delete")


class Seller(User):
    __tablename__ = "seller_table"

    id: Mapped[intpk] = mapped_column(ForeignKey("user_table.id", ondelete="CASCADE"), primary_key=True)

    __mapper_args__ = {"polymorphic_identity": "seller_table"}

    # relationship
    # listes des clients gerer( one-to-many)
    customers: Mapped[list["Customer"]] = relationship(back_populates="seller_contact")
    # listes des contrats gerer( one-to-many)
    contracts: Mapped[list["Contract"]] = relationship(back_populates="seller")

    def attribute_to_display(self) -> list:
        """Function return all attribute available to be displayed, including additional attributes."""
        list_attributes = super().attribute_to_display()
        add_attributes = ["customers", "contracts"]
        return list_attributes + add_attributes

    def get_all_clients_of_user(self, session) -> list:
        # Function return all clients of user.
        customers_list = session.scalars(select(Customer).where(Customer.seller_contact == session.current_user)).all()
        return customers_list

    def get_all_contracts_of_user(self, session) -> list:
        # Function return all contracts of user.
        contracts_list = session.scalars(select(Contract).where(Contract.seller == session.current_user)).all()
        return contracts_list

    def get_all_contracts_of_user_without_event(self, session) -> list:
        # The function returns all contracts signed by the seller that are not linked to an event.
        available_contracts_list = session.scalars(
            select(Contract).where(
                (Contract.seller_id == session.current_user.id)
                & (Contract.signed_contract == True)  # noqa
                & (Contract.event == None)  # noqa
            )
        ).all()
        return available_contracts_list

    def get_unsigned_contracts(self, session) -> list:
        # Function return all unsigned contracts managed by current user.
        unsigned_contracts_list = session.scalars(
            select(Contract).where(
                (Contract.seller == session.current_user) & (Contract.signed_contract == False)  # noqa
            )
        ).all()
        return unsigned_contracts_list

    def get_unpayed_contracts(self, session) -> list:
        # Function return all unpayed contracts managed by current user.
        unpayed_contracts_list = session.scalars(
            select(Contract).where((Contract.seller == session.current_user) & (Contract.remaining > 0))
        ).all()
        return unpayed_contracts_list

    def create_new_customer(self, session, customer_info: dict) -> Customer:
        try:
            new_customer = Customer(
                name=customer_info["name"],
                email_address=customer_info["email_address"],
                phone_number=customer_info["phone_number"],
                company=customer_info["company"],
                seller_contact=session.current_user,
            )
            session.add(new_customer)
        except (KeyError, ValueError):
            return None
        else:
            return new_customer

    def create_new_event(self, session, event_info: dict) -> Event:
        """
        Function add a new event to database.

        Args:
            session (_type_): _description_
            event_info (_type_): _description_
        """
        try:
            # get customer of new event.
            customer = event_info["contract"].customer
            new_event = Event(
                name=event_info["name"],
                date_start=event_info["date_start"],
                date_end=event_info["date_end"],
                attendees=event_info["attendees"],
                note=event_info["note"],
                contract=event_info["contract"],
                supporter=event_info["supporter"],
                address=event_info["address"],
            )
            new_event.customer = customer
            session.add(new_event)

        except (KeyError, ValueError):
            return None
        else:
            return new_event

    def update_customer(self, customer: Customer, attribute_update: str, new_value) -> None:
        """
        Function updates an attribute of Customer.
        If attribute update is in the forbidden attribut, the function pass and customer will be bot updated.
        forbidden_attribut = ["created_date", "events", "contracts"]

        Args:
            session (_type_): _description_
            customer (Customer): Instance of Customer class to be updated.
            attribute_update (str): Attribute of Instance to be updated.
            new_value (_type_): New value of attribute to be updated.
        """
        forbidden_attribut = ["created_date", "events", "contracts"]
        if attribute_update not in forbidden_attribut:
            setattr(customer, attribute_update, new_value)
            customer.set_updated_date()
        else:
            pass

    def update_contract(self, contract: Contract, attribute_update: str, new_value) -> None:
        """
        Function update an attribut of contract.
        If attribute update is in the forbidden attribut, the function pass and customer will be bot updated.
        forbidden_attribut= ["created_date", "seller", "seller_id", "events", "customer", "customer_id"]
        Args:
            session (_type_): _description_
            contract (Contract): Instance of Contract class to be updated.
            attribute_update (str):  Attribute of Instance to be updated.
            new_value (_type_): New value of attribute to be updated.
        """
        forbidden_attribut = ["created_date", "seller", "seller_id", "event", "customer", "customer_id"]
        if attribute_update not in forbidden_attribut:
            setattr(contract, attribute_update, new_value)
            if attribute_update == "signed_contract":
                logger.info(f"{contract} has been signed!")
        else:
            pass
