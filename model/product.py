from pydantic import BaseModel


class ProductModel(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
