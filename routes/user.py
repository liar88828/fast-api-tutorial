from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from controller.user import UserController
from database.connect import get_db
from schema.response import Response
from schema.user import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])
user_controller = UserController()


@router.get('/')
async def user_find_all(db: AsyncSession = Depends(get_db)):
    result = await  user_controller.find_all(db)
    return Response(message="success get all data user", data=result, code=200)


@router.get('/{id_user}')
async def user_find_one(id_user: int, db: AsyncSession = Depends(get_db)):
    result = await user_controller.find_by_id(db, id_user)
    return Response(code=201, message=f'success get data by id {id_user}', data=result, )


@router.post('/')
async def user_create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await user_controller.create(db, user)
    return Response(code=200, message=f'success create user', data=result, )


@router.put('/{id_user}')
async def user_update(user: UserUpdate, id_user: int, db: AsyncSession = Depends(get_db)):
    result = await user_controller.update(db, id_user, user)
    return Response(code=200, message=f'success update user {id_user}', data=result)


@router.delete('/{id_user}')
async def user_delete(id_user: int, db: AsyncSession = Depends(get_db)):
    result = await user_controller.delete(db, id_user)
    return Response(code=200, message=f'success delete user {id_user}', data=result)
