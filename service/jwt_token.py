from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from schema.user import UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
import jwt

from key import JWT_SECRET_ACCESS_KEY, JWT_ALGORITHM


# expire = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=expires_delta)

def create_jwt(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_ACCESS_KEY, algorithm=JWT_ALGORITHM)


def verify_jwt(token: str = Depends(oauth2_scheme)) -> UserDB:
    try:
        payload: UserDB = jwt.decode(token, JWT_SECRET_ACCESS_KEY, algorithms=[JWT_ALGORITHM])
        # username = payload.get("username")
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        # return {"message": f"Hello, {username}! This is secure data."}
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
