from datetime import date
from typing import Optional, List
from uuid import UUID

from models.base import BaseModel


# class Person(BaseModel):
#     """Описание модели человека."""
#     full_name: str
#     birth_date: Optional[date]

class Person(BaseModel):
    id: str
    name: Optional[str]
