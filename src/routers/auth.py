
from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from hasher import Hasher
import Oauth2
from sqlalchemy import text


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    

    query = await db.execute(
        text("SELECT * FROM users WHERE email = :email"), {"email": user_cred.username}
        )
    user = query.fetchone()
    if user:
        user = user._asdict()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Creadentials")
    # Add password verification and token generation logic here
    if not Hasher.verify_password(user_cred.password,user["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid Credentials")
    data = {}
    data["id"] = user["id"]
    token = Oauth2.create_jwt_token(data)
    
    return schemas.Token(token=token,token_type="Bearer")
    