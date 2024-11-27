from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


# @dataclass
class ProductSchema(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None


class ProductCreate(ProductSchema):
    pass


class ProductUpdate(ProductSchema):
    pass


class Product(ProductSchema):
    id: int

    class Config:
        orm_mode = True
