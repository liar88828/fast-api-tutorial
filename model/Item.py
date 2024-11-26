from typing import Union
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_sell: Union[bool, None] = None


