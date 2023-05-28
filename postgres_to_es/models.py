
import os
from dotenv import load_dotenv
from typing import List, Optional
from pydantic import BaseModel

load_dotenv()


class DSL(BaseModel):
    dbname: str = os.environ.get('DBNAME')
    user: str = os.environ.get('DBUSER')
    password: str = os.environ.get('PASSWORD')
    host: str = os.environ.get('HOST')
    port: int = int(os.environ.get('PORT'))


class Elastic(BaseModel):
    host: str = os.environ.get('ELHOST')
    port: int = int(os.environ.get('ELPORT'))


class Person(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: Optional[float] = None
    genre: List[str]
    title: str
    description: Optional[str] = None


class FilmWork(Film):
    director: List[str]
    actors_names: List[str]
    writers_names: List[str]
    actors: List[Person]
    writers: List[Person]
