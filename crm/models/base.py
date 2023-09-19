import datetime
from typing_extensions import Annotated
from sqlalchemy import Integer, MetaData, String, func
from sqlalchemy.orm import DeclarativeBase, mapped_column

my_metadata = MetaData()

intpk = Annotated[int, mapped_column(Integer(), primary_key=True, autoincrement=True)]
required_name = Annotated[str, mapped_column(String(50), nullable=False)]
timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
]


class Base(DeclarativeBase):
    metadata = my_metadata
