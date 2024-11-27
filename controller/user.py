from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.table.user import UserTable
from schema.user import UserCreate


class UserController:
    async def find_all(self, db: AsyncSession):
        result = await db.execute(select(UserTable))
        return result.scalars().all()

    async def find_by_id(self, db: AsyncSession, id_user: int):
        result = await db.execute(select(UserTable).where(UserTable.id == id_user))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create(self, db: AsyncSession, user: UserCreate):
        new_user = UserTable(**user.dict())
        db.add(new_user)
        await  db.commit()
        await db.refresh(new_user)
        return new_user

    async def update(self, db: AsyncSession, id_user: int, user: UserCreate, ):
        exist_user = await self.find_by_id(db, id_user)
        if exist_user:
            for key, value in user.dict().items():
                setattr(exist_user, key, value)
            db.add(exist_user)
            await db.commit()
            await db.refresh(exist_user)
            return exist_user

    async def delete(self, db: AsyncSession, id_user: int):
        exist_user = await self.find_by_id(db, id_user)
        if exist_user:
            await db.delete(exist_user)
            await db.commit()
            return exist_user
