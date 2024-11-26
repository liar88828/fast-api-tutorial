from typing import Union

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.config import get_db
from database.table import ProductTable
from model.Item import Item
from model.product import ProductModel

app = FastAPI()


@app.get("/")
async def read_root(db: AsyncSession = Depends(get_db)):
    # Use the `db` object here
    return {"message": "Database session is ready"}


@app.get('/products')
async def get_product(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductTable))
    product = result.scalars().all()
    return {'product': product}


@app.get('/product/{id_product}')
async def get_product_byid(id_product: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductTable).where(ProductTable.id == id_product))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@app.post('/product', response_model=dict)
async def create_product(
        product: ProductModel,
        db: AsyncSession = Depends(get_db)
):
    new_product = ProductTable(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return {'message': "product created successfully", 'product': product}


@app.put('/product/{id_product}')
async def update_product(id_product: int, product: ProductModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductTable).where(ProductTable.id == id_product))
    productResult = result.scalar_one_or_none()
    if not productResult:
        raise HTTPException(status_code=404, detail="product not found")
    productResult.name = product.name
    productResult.description = product.description
    productResult.price = product.price
    productResult.quantity = product.quantity
    await db.commit()
    return {'message': "product updated successfully"}


@app.delete('/product/{id_product}')
async def delete_product(id_product: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProductTable).where(ProductTable.id == id_product))
    productResult = result.scalar_one_or_none()
    if not productResult:
        raise HTTPException(status_code=404, detail="Product not found")
    await db.delete(productResult)
    await db.commit()
    return {'message': "product deleted successfully"}

# -------------------
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get('/items/{id_item}')
async def read_item(id_item: int, q: Union[bool, None] = None):
    return {"item_id": id_item, "is_sell": q}


@app.post("/items")
async def create_item(item: Item):
    return {"item": item}


@app.put('/items/{id_item}')
async def update_item(id_item: int, item: Item):
    return {"id_item": id_item, "item": item}


@app.delete('/items/{id_item}')
async def delete_item(id_item: int):
    return {"id_item": id_item}
