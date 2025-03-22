from datetime import datetime, timedelta
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from sqlalchemy.ext.asyncio import AsyncSession


import schemas
from database import get_db
from models import UserModel
from dotenv import load_dotenv
import os
load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
TOKEN_EXPIRATION_TIME = int(os.getenv("TOKEN_EXPIRATION_TIME"))
TOKEN_ALGORITHM = os.getenv("TOKEN_ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_jwt_token(data: dict):
    expire = datetime.now() + timedelta(minutes=TOKEN_EXPIRATION_TIME)
    data["exp"] = int(expire.timestamp())
    
    token = jwt.encode(data, JWT_SECRET, algorithm=TOKEN_ALGORITHM)
    return token

def verify_jwt_token(token: str, invalid_credential: HTTPException):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[TOKEN_ALGORITHM])
        user_id = payload.get("id")
        if user_id is None:
            raise invalid_credential
        return user_id
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError:
        raise invalid_credential

async def get_current_user(token: str = Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    invalid_credential = HTTPException(status_code=401, detail="Invalid credentials")
    id = verify_jwt_token(token, invalid_credential)
    user = await db.get(UserModel,id)
    return user
    
    
    
    