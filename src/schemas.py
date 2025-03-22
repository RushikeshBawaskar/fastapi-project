from pydantic import BaseModel, EmailStr

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
    class Config:
        orm_mode = True
    
    
    

class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    class Config:
        orm_mode = True
    
    
class Token(BaseModel):
    token: str
    token_type: str
    
    
class TokenData(BaseModel):
    id:int
    