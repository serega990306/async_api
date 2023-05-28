
import logging
from backoff import backoff
from elasticsearch import Elasticsearch, helpers

from models import Elastic


class ElasticConnector:

    @backoff(message='Ошибка подключения к Elasticsearch')
    def connect(self) -> Elasticsearch:
        """
        Функция для создания подключения к Elasticsearch
        :return: объект Elasticsearch
        """
        data = Elastic()
        return Elasticsearch(f'http://{data.host}:{data.port}')

    def add(self, body: list) -> bool:
        """
        Функция для создания подключения к Elasticsearch
        :param body: список фильмов
        :return: флаг успешности добавления данных
        """
        conn = self.connect()
        try:
            helpers.bulk(conn, body, index='movies')
            logging.info('Данные успешно добавлены в Elasticsearch!')
            return True
        except Exception as err:
            logging.error(f'Ошибка добавления данных в Elasticsearch\n{type(err)}\n{err}')
            return False
