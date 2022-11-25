from sqlalchemy import Column, DateTime, String, func, UniqueConstraint, Date, Integer, ForeignKey, ForeignKeyConstraint

from .base import Base


class CustomerType(Base):
    __tablename__ = "customer_type"
    __table_args__ = {"schema": "foo"}

    id = Column(Integer, primary_key=True)
    code = Column(String(32), comment="customer type code", nullable=False)


class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"schema": "foo"}

    primary_key = Column(String(32), primary_key=True, comment="UID")
    first_name = Column(String(100), comment="First name", nullable=False)
    last_name = Column(String(100), comment="Last name", nullable=False)
    customer_type_id = Column(Integer, ForeignKey("foo.customer_type.id"))
