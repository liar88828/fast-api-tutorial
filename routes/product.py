from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from controller.product import ProductController
from database.connect import get_db
from schema.product import ProductCreate, ProductUpdate
from schema.response import Response
from schema.user import UserDB
from service.jwt_token import verify_jwt

product_controller = ProductController()
app = FastAPI()
router = APIRouter(prefix="/products", tags=["products"], )


# @router.middleware("http")
# async def product_token_verification_middleware(request: Request, call_next):
#     return await verify_access_token(request, call_next)


@router.get('/')
async def product_all(db: AsyncSession = Depends(get_db)):
    response_db = await product_controller.find_all(db)
    return Response(code=200, message='success', data=response_db)


@router.get('/{id_product}')
async def product_one(id_product: int, db: AsyncSession = Depends(get_db)):
    result = await product_controller.find_by_id(db, id_product)
    return Response(data=result, code=201, message=f"success get product by id:{id_product}")


@router.post('/')
async def product_create(product: ProductCreate,
                         db: AsyncSession = Depends(get_db),
                         user: UserDB = Depends(verify_jwt)
                         ):
    product_data = product.model_copy(update={"id_user": user['id']})
    response_db = await product_controller.create(db=db, product=product_data)
    return Response(data=response_db, message="success create", code=200)


@router.put('/{id_product}')
async def product_update(product: ProductUpdate, id_product: int,
                         db: AsyncSession = Depends(get_db),
                         user: UserDB = Depends(verify_jwt)
                         ):
    product_data = product.model_copy(update={"id_user": user['id']})
    result = await product_controller.update(db=db, id_product=id_product, product=product_data)
    return Response(code=200, message="success update", data=result)


@router.delete('/{id_product}')
async def product_delete(id_product: int,
                         db: AsyncSession = Depends(get_db),
                         user: UserDB = Depends(verify_jwt)
                         ):
    result = await product_controller.delete(db=db, id_product=id_product, id_user=user['id'])
    return Response(code=200, message="success delete", data=result)
