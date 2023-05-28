import orjson
from typing import List, Optional

from models.base import BaseModel
from models.person import Person


# class Film(BaseModel):
#     """Описание модели кинопроизведений."""
#     title: str
#     description: str
#     imdb_rating: float
#     genre: List[str]
#     actors: List[str]
#     writers: List[str]
#     directors: List[str]


class Film(BaseModel):
    id: str
    imdb_rating: Optional[float] = None
    genre: List[str]
    title: str
    description: Optional[str] = None
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[Person]
    writers: List[Person]
