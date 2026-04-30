from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List
from src.book.schemas import Book
from src.review.schemas import ReviewModel

class UserCreatemodel(BaseModel):
    username:str = Field(max_length=8)
    email:str = Field(max_length=40)
    first_name:str = Field(max_length=25)
    last_name:str = Field(max_length=25)
    password:str = Field(min_length=6)

class UserModel(BaseModel):
    uid:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    password_hash:str = Field(exclude=True)
    is_verified:bool
    created_at:datetime
    updated_at:datetime

class UserBooksModel(UserModel):
    books:List[Book]
    reviews:List[ReviewModel]

class UserLoginmodel(BaseModel):
    email:str = Field(max_length=40)
    password:str = Field(min_length=6)

