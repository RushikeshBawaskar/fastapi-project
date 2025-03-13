from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import Post
from models import PostModel
from database import get_db
from fastapi import Response
from typing import List

router = APIRouter(tags=["Posts"])


@router.get("/posts/", response_model=List[Post])
async def read_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PostModel))
    posts = result.scalars().all()
    return posts

@router.get("/posts/{id}")
async def find_post(id: int,db:AsyncSession=Depends(get_db)):
    post = await db.get(PostModel,id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="resource not found")
    return {"response": post, "message": "Resource found successfully in database"}

            

@router.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post,db:AsyncSession=Depends(get_db)):
    
    new_post = PostModel(title=post.title,content=post.content,published=post.published)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    
    return {"response": new_post, "message": "Post created"}

@router.put("/posts/{id}")
async def update_post(id: int, post: Post, db: AsyncSession = Depends(get_db)):
    existing_post = await db.get(PostModel, id)
    if not existing_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource not found with id {id}")
    
    existing_post.title = post.title
    existing_post.content = post.content
    existing_post.published = post.published
    
    await db.commit()
    await db.refresh(existing_post)
    
    return {"response": existing_post, "message": "Post updated successfully"}

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(PostModel, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resource not found with id {id}")
    
    await db.delete(post)
    await db.commit()
    
    return {"message": "Post deleted successfully"}