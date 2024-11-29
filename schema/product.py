from typing import Optional

from pydantic import BaseModel


# @dataclass
class ProductSchema(BaseModel):
    name: str
    price: float
    quantity: int
    description: Optional[str] = None
    id_user: Optional[int] = None


class ProductCreate(ProductSchema):
    pass


class ProductUpdate(ProductSchema):
    pass


class ProductDB(ProductSchema):
    id: int

    class Config:
        from_attributes = True
