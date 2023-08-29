import factory
import datetime
from models.users import Manager, Seller, Supporter, User


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: "%s" % n)


class ManagerFactory(UserFactory):
    class Meta:
        model = Manager

    name = factory.Sequence(lambda n: "manager%d" % n)
    phone_number = "+330000000"
    created_date = factory.LazyFunction(datetime.now)
    password = "password"

    @factory.lazy_attribute
    def email_address(self):
        return "%s@example.com" % self.username


class SellerFactory(UserFactory):
    class Meta:
        model = Seller

    name = factory.Sequence(lambda n: "seller%d" % n)
    phone_number = "+330000000"
    created_date = factory.LazyFunction(datetime.now)
    password = "password"

    @factory.lazy_attribute
    def email_address(self):
        return "%s@example.com" % self.username


class SupporterFactory(UserFactory):
    class meta:
        model = Supporter

    name = factory.Sequence(lambda n: "supporter%d" % n)
    phone_number = "+330000000"
    created_date = factory.LazyFunction(datetime.now)
    password = "password"

    @factory.lazy_attribute
    def email_address(self):
        return "%s@example.com" % self.username
