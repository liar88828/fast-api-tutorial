from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class Product(UserBase):
    id: int

    class Config:
        orm_mode = True
