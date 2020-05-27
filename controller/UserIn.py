from pydantic import BaseModel

class UserBase(BaseModel):
    id: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    book: str
    is_active: bool

    class Config:
        orm_mode = True
