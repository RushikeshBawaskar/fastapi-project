
from pydantic import EmailStr
from sqlalchemy import Boolean, Column, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP



Base = declarative_base()


class PostModel(Base):
    __tablename__ ="posts"
    
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default="TRUE")
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'), onupdate=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=text('now()'))
    
    
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'), onupdate=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=text('now()'))
    
    
