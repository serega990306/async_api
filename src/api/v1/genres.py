from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.genre import GenreService, get_genre_service

router = APIRouter()


class Genre(BaseModel):
    id: str
    name: str


@router.get('/{genre_id}',
            response_model=Genre,
            summary="Информация о жанрах",
            description="Полнотекстовый поиск по кинопроизведениям",
            response_description="Название жанра"
            )
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> Genre:
    film = await genre_service.get_by_id(genre_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(id=film.id, name=film.name)
