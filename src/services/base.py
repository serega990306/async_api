from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre

GENRE_CACHE_EXPIRE_IN_SECONDS = 360  # 1 час


class BaseService:

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, object_id: str) -> Optional[Genre]:
        genre = await self._genre_from_cache(object_id)
        if not genre:
            genre = await self._get_genre_from_elastic(object_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)

        return genre