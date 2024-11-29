from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from controller.user import UserController
from database.connect import get_db
from database.table.user import UserTable
from schema.user import UserCreate, UserLogin
from service.jwt_token import verify_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


class AuthController(UserController):
    async def authenticate(self, db: AsyncSession, token: str):
        user = verify_jwt(token)
        response = await db.execute(UserTable.select().where(UserTable.c.id == user.id))
        exist = await response.scalar_one_or_none()
        if not exist:
            raise HTTPException(status_code=404, detail="User not found")
        return exist

    async def register(self, db: AsyncSession, user: UserCreate):

        email_exist = await self.find_by_email(db, user.email)
        if email_exist:
            raise HTTPException(400, detail="Email already registered")

        user.password = get_password_hash(user.password)
        user_db = await self.create(db, user)

        user_dict = await self.user_convert(user_db)
        return user_dict

    async def login(self, db: AsyncSession, user: UserLogin):

        user_db = await self.find_by_email(db, user.email)
        if not user_db:
            raise HTTPException(status_code=404, detail="Email not found")

        valid_password = verify_password(user.password, user_db.password)
        if not valid_password:
            raise HTTPException(status_code=401, detail="Incorrect password")

        user_dict = await self.user_convert(user_db)
        return user_dict

    async def user_convert(self, user_db):
        # Convert to a dictionary if it's a model instance
        if hasattr(user_db, "__dict__"):
            user_dict = user_db.__dict__.copy()  # Avoid modifying the original object
        else:
            raise ValueError("Unexpected type for user_db; expected an object with a __dict__ attribute.")
        # Remove sensitive fields
        user_dict.pop("password", None)
        user_dict.pop("_sa_instance_state", None)
        return user_dict
