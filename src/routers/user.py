
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from hasher import Hasher
import dto
from schemas import User
from models import UserModel
from database import get_db


router = APIRouter(tags=["User"])

@router.post("/users",status_code=status.HTTP_201_CREATED, response_model=dto.User)
async def create_user(user: User, db: AsyncSession = Depends(get_db)):
    try:
        user.password = Hasher.get_password_hash(user.password)
        new_user = UserModel(
            **user.model_dump() # Make sure to hash the password before storing it
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        if "unique constraint" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        raise e

@router.get("/users/{id}",response_model=dto.User)
async def get_user(id:int,db:AsyncSession=Depends(get_db)):
    user = await db.get(UserModel, id)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found for id {id}")
    
    return user