from sqlmodel import SQLModel, Field, Session
from typing import Optional

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    todo_name: str
    is_complete: bool = False




# # create database schema
# class Todo(SQLModel, table=True):
#     id : Optional[int] = Field(default=None, primary_key=True)
#     todo_name : str
#     is_complete : bool = False

