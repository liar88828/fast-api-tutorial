from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.table.product import ProductTable
from schema.product import ProductCreate, ProductUpdate


# noinspection PyMethodMayBeStatic
class ProductController:
    # def __init__(self, db: AsyncSession):
    #     self.db = db

    async def find_all(self, db: AsyncSession):
        result = await db.execute(select(ProductTable))
        return result.scalars().all()

    async def find_by_id(self, db: AsyncSession, id_product: int):
        result = await db.execute(select(ProductTable).where(id_product == ProductTable.id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        return product

    async def create(self, db: AsyncSession, product: ProductCreate):
        new_product = ProductTable(**product.model_dump())
        # new_product = Product(
        #     name=product.name,
        #     description=product.description,
        #     price=product.price,
        #     quantity=product.quantity
        # )
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product

    async def update(self, db: AsyncSession, id_product: int, product: ProductUpdate, ):
        existing_product = await self.find_by_id(db, id_product)
        if existing_product:
            for key, value in product.model_dump().items():
                setattr(existing_product, key, value)
            db.add(existing_product)
            await db.commit()
            await db.refresh(existing_product)
            return existing_product

    async def delete(self, db: AsyncSession, id_product: int, id_user: int):
        product = await self.find_by_id(db, id_product)
        if product.id_user != id_user:
            raise HTTPException(status_code=400, detail="You do not have permission to delete this product")

        if product:
            await db.delete(product)
            await db.commit()
            return product
