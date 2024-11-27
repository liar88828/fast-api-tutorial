from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.table.product import ProductTable
from schema.product import ProductCreate, ProductUpdate


class ProductController:

    async def find_all(self, db: AsyncSession):
        result = await db.execute(select(ProductTable))
        return result.scalars().all()

    async def find_by_id(self, db: AsyncSession, id_product: int):
        result = await db.execute(select(ProductTable).where(ProductTable.id == id_product))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="product not found")
        return product

    async def create(self, db: AsyncSession, product: ProductCreate):
        new_product = ProductTable(**product.dict())
        # new_product = ProductTable(
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
            for key, value in product.dict().items():
                setattr(existing_product, key, value)
            db.add(existing_product)
            await db.commit()
            await db.refresh(existing_product)
            return existing_product

    async def delete(self, db: AsyncSession, id_product: int):
        product = await self.find_by_id(db, id_product)
        if product:
            await db.delete(product)
            await db.commit()
            return product