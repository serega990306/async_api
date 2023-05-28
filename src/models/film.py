
from typing import List, Optional

from models.base import BaseModel
from models.person import Person


class Film(BaseModel):
    """Описание модели кинопроизведений."""
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
