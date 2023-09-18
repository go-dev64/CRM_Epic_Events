import factory
from datetime import datetime

import sqlalchemy
from crm.models.users import Manager, Seller, Supporter, User
import tests.conftest


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: "%s" % n)
    name = factory.Sequence(lambda n: "user%d" % n)
    phone_number = factory.Faker("phone_number")
    created_date = factory.LazyFunction(datetime.now)
    password = "password"

    @factory.lazy_attribute
    def email_address(self):
        return "%s@example.com" % self.name


class ManagerFactory(UserFactory):
    class Meta:
        model = Manager


class SellerFactory(UserFactory):
    class Meta:
        model = Seller


class SupporterFactory(UserFactory):
    class meta:
        model = Supporter
