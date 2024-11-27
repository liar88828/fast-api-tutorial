from typing import Union

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from dataclasses import dataclass

Base = declarative_base()


# @dataclass
class ProductTable(Base):
    __tablename__ = 'products'

    # id: int
    # name: str
    # price: float
    # quantity: int
    # description: Union[str]

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
