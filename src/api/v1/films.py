from http import HTTPStatus
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class Person(BaseModel):
    id: str
    name: str


class ShortFilm(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float] = None


class Film(ShortFilm):
    genre: List[str]
    description: Optional[str] = None
    director: List[str]
    actors: List[Person]
    writers: List[Person]


@router.get('/search',
            response_model=List[ShortFilm],
            summary="Список кинопроизведений",
            description="Сортированный список кинопроизведений",
            response_description="Список данных о фильмах"
            )
async def film_search(query: str,
                      film_service: FilmService = Depends(get_film_service),
                      page: int = Query(ge=0, default=0),
                      size: int = Query(ge=1, le=50, default=50)) -> List[ShortFilm]:
    films = await film_service.get(query=query, page_from=page, page_size=size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    _film_list = list([ShortFilm(uuid=film.id, imdb_rating=film.imdb_rating, title=film.title) for film in films])

    return _film_list


@router.get('/{film_id}',
            response_model=Film,
            summary="Информация о кинопроизведении",
            description="Полная информация о кинопроизведении",
            response_description="Данные фильма"
            )
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(uuid=film.id, imdb_rating=film.imdb_rating, title=film.title, genre=film.genre,
                description=film.description, director=film.director, actors=film.actors, writers=film.writers)


@router.get('/',
            response_model=List[ShortFilm],
            summary="Список кинопроизведений",
            description="Сортированный список кинопроизведений",
            response_description="Список данных о фильмах"
            )
async def film_list(film_service: FilmService = Depends(get_film_service),
                    genre: Union[str, None] = None,
                    page: int = Query(ge=0, default=0),
                    size: int = Query(ge=1, le=50, default=50)) -> List[ShortFilm]:
    films = await film_service.get(genre=genre, page_from=page, page_size=size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='films not found')

    _film_list = list([ShortFilm(uuid=film.id, imdb_rating=film.imdb_rating, title=film.title) for film in films])

    return _film_list



