
from models.base import BaseModel


class Genre(BaseModel):
    """Описание модели жанров кинопроизведений."""
    id: str
    name: str
