from sqlmodel import SQLModel, Field, Column, Relationship
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import List
from src.book import models

class User(SQLModel, table=True):
    __tablename__ = 'users'

    uid:uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid.uuid4))
    username:str
    email:str
    first_name:str
    last_name:str
    password_hash:str = Field(exclude=True)
    role:str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default='user'))
    is_verified:bool = Field(default=False)
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    books:List["models.Book"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})

    def __repr__(self):
        return f"<user {self.username}>"


