
from sqlalchemy import Boolean, Column, Integer, String, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship



Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'), onupdate=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=text('now()'))
    
    
class PostModel(Base):
    __tablename__ ="posts"
    
    id = Column(Integer, primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean, server_default="TRUE")
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'), onupdate=text('now()'))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    
    owner = relationship(UserModel)

    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    
    
    
