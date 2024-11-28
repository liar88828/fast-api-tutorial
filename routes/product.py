from fastapi import Depends, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from database.connect import get_db
from schema.product import  ProductCreate, ProductUpdate
from controller.product import ProductController
from schema.response import Response

router = APIRouter(prefix="/products", tags=["products"])
product_controller = ProductController()


@router.get('/')
async def product_all(db: AsyncSession = Depends(get_db)):
    responseDB = await product_controller.find_all(db)
    return Response(code=200, message='success', data=responseDB)


@router.get('/{id_product}')
async def product_one(id_product: int, db: AsyncSession = Depends(get_db)):
    result = await product_controller.find_by_id(db, id_product)
    return Response(data=result, code=201, message=f"success get product by id:{id_product}")


@router.post('/')
async def product_create(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    responseDb = await product_controller.create(db=db, product=product)
    return Response(data=responseDb, message="success create", code=200)


@router.put('/{id_product}')
async def product_update(id_product: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)):
    result = await product_controller.update(db=db, id_product=id_product, product=product)
    return Response(code=200, message="success update", data=result)


@router.delete('/{id_product}')
async def product_delete(id_product: int, db: AsyncSession = Depends(get_db)):
    result = await product_controller.delete(db=db, id_product=id_product)
    return Response(code=200, message="success delete", data=result)
