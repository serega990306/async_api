from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.person import PersonService, get_person_service

router = APIRouter()


class Film(BaseModel):
    id: str
    roles: List[str]


class Person(BaseModel):
    id: str
    full_name: str
    films: Optional[List[Film]]


@router.get('/{person_id}',
            response_model=Person,
            summary="Информация о персоналиях",
            description="Информация о персоналии с фильмографией",
            response_description="Полное имя и роли в фильмах"
            )
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(id=person.id, full_name=person.full_name, films=person.films)


@router.get('/{person_id}/film',
            response_model=Person,
            summary="Информация о персоналиях",
            description="Информация о персоналии с фильмографией",
            response_description="Полное имя и роли в фильмах"
            )
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(id=person.id, full_name=person.full_name, films=person.films)