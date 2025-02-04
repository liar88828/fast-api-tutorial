from pydantic import BaseModel

from schema.my_enum import RoleUser


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


class UserDB(UserBase):
    id: int
    role: RoleUser

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str
    password: str
