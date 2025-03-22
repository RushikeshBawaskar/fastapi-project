from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Post, TokenData, User
from models import PostModel, UserModel
from database import get_db
from fastapi import Response
from typing import List

from Oauth2 import get_current_user

router = APIRouter(tags=["Posts"])


@router.get("/posts/", response_model=List[Post])
async def read_posts(db: AsyncSession = Depends(get_db),user:User=Depends(get_current_user)):
    result = await db.execute(select(PostModel))
    posts = result.scalars().all()
    return posts

@router.get("/posts/{id}")
async def find_post(id: int,db:AsyncSession=Depends(get_db),user:TokenData=Depends(get_current_user)):
    post = await db.get(PostModel,id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="resource not found")
    return {"response": post, "message": "Resource found successfully in database"}

            

@router.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post,db:AsyncSession=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    new_post = PostModel(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    
    return {"response": new_post, "message": "Post created"}

@router.put("/posts/{id}")
async def update_post(id: int, post: Post, db: AsyncSession = Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    existing_post = await db.get(PostModel, id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource not found with id {id}")
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not allowed to update the post")
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    
    await db.commit()
    await db.refresh(existing_post)
    
    return {"response": existing_post, "message": "Post updated successfully"}

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    post = await db.get(PostModel, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource not found with id {id}")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not allowed to delete the post")
        
    await db.delete(post)
    await db.commit()
    
    return {"message": "Post deleted successfully"}