from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    name: str
    email: str
    created_at: datetime
    updated_at: datetime