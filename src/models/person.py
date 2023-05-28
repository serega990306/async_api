
from typing import Optional

from models.base import BaseModel


class Person(BaseModel):
    """Описание модели человека."""
    id: str
    name: Optional[str]
