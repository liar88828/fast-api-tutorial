from fastapi import Depends, APIRouter

from service.jwt_token import create_jwt,  verify_jwt

router = APIRouter(prefix="/token", tags=["token"])
users_db = {
    "username": "user1",
    "password": "password123"
}


@router.post("/")
async def login():
    return create_jwt(data=users_db)


@router.get("/")
async def read_users_me(token: dict = Depends(verify_jwt)):
    return token
