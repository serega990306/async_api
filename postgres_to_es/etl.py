
import logging
import datetime
import psycopg2
from time import sleep
from psycopg2.extras import DictCursor

from backoff import backoff
from storage import State, JsonFileStorage
from models import FilmWork, Film, Person, DSL
from elastic import ElasticConnector


logging.basicConfig(filename=f'ETLManager.log', encoding='utf-8', level=logging.INFO)


class ETLManager:
    state = State(JsonFileStorage('storage.txt'))
    elastic = ElasticConnector()
    cur = None

    def run(self) -> None:
        """
        Функция запуска ETL процесса
        :return:
        """
        logging.info(f'ETL Manager запущен...')
        tables = ['film_work', 'person', 'genre', 'genre_film_work', 'person_film_work']
        while True:
            for name in tables:
                self.producer(name)
            sleep(5)

    @backoff(message='Ошибка подключения к Postgres')
    def connect(self):
        """
        Функция подключению к БД
        :return:
        """
        pg_conn = psycopg2.connect(**DSL().dict(), cursor_factory=DictCursor)
        return pg_conn

    def producer(self, name: str) -> None:
        """
        Функция получения идентификаторов обновленных записей из заданной таблицы
        :param name: наименование таблицы
        :return:
        """
        pg_conn = None
        etl_dt = self.state.get_state('etl')
        if not etl_dt:
            md = datetime.datetime(1970, 6, 16, 20, 14, 9, 310212, tzinfo=datetime.timezone.utc)
        else:
            md = datetime.datetime.strptime(etl_dt, '%Y-%m-%d %H:%M:%S.%f%z')
        try:
            pg_conn = self.connect()
            with pg_conn:
                self.cur = pg_conn.cursor
                with self.cur() as cursor:
                    cursor.execute(f"""SELECT id FROM content.{name} where modified > '{md}' ORDER BY modified;""")
                    while True:
                        result = cursor.fetchmany(10)
                        if result:
                            logging.info(f'Получены данные из таблицы {name}')
                            ids = list()
                            for row in result:
                                ids.append(row['id'])
                            if name != 'film_work':
                                ids = self.get_film_ids(ids, name)
                            self.collect_films(ids)
                        else:
                            logging.info(f'Синхранизация таблицы {name} завершена!')
                            break
        except Exception as err:
            logging.error(f'Ошибка получения данных из таблицы {name}\n{type(err)}\n{err}')
        finally:
            if pg_conn:
                pg_conn.close()

    def get_film_ids(self, ids: list, name: str) -> list:
        """
        Функция получения связанных идентификаторов фильмов
        :param ids: список идентификаторов обновленных записей
        :param name: наименование таблицы
        :return: список идентификаторов фильмов
        """
        with self.cur() as cursor:
            mapping = {'person': ['person_film_work', 'person_id'],
                       'person_film_work': ['person_film_work', 'id'],
                       'genre': ['genre_film_work', 'genre_id'],
                       'genre_film_work': ['genre_film_work', 'id']}
            query = f"""SELECT film_work_id FROM content.{mapping[name][0]} WHERE {mapping[name][1]} in {tuple(ids)};"""
            cursor.execute(query)
            result = cursor.fetchall()
            film_ids = list()
            for row in result:
                film_ids.append(row['film_work_id'])
            return film_ids

    def collect_films(self, ids: list) -> None:
        """
        Функция получения данных о фильмах
        :param ids: список идентификаторов фильмов
        :return:
        """
        with self.cur() as cursor:
            cursor.execute(f"""SELECT
                                    fw.id, 
                                    fw.title, 
                                    fw.description,
                                    fw.rating as imdb_rating, 
                                    array_agg(DISTINCT g.name) as genre
                                FROM content.film_work fw 
                                LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
                                LEFT JOIN content.genre g ON g.id = gfw.genre_id
                                where fw.id in {tuple(ids)}
                                GROUP BY fw.id
                                ORDER BY fw.modified;""")

            result = cursor.fetchall()
            if result:
                film_list = list()
                for row in result:
                    film = Film(**row)
                    film_list.append(film)
                self.enricher(film_list)

    def enricher(self, film_list: list) -> None:
        """
        Функция дополнения информации о фильмах
        :param film_list: список объектов фильмов
        :return:
        """
        with self.cur() as cursor:
            query = """SELECT p.id, p.full_name, pfw.role, fw.modified FROM content.film_work fw
                                        INNER JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
                                        INNER JOIN content.person p ON pfw.person_id = p.id
                                        WHERE pfw.film_work_id = '{}'
                                        ORDER BY fw.modified;"""

            film_work_list = list()
            last_modified = ''
            for film in film_list:
                actors = list()
                writers = list()
                director = list()
                cursor.execute(query.format(str(film.id)))
                result = cursor.fetchall()
                for row in result:
                    if row['role'] == 'actor':
                        actors.append(Person(id=row['id'], name=row['full_name']))
                    elif row['role'] == 'writer':
                        writers.append(Person(id=row['id'], name=row['full_name']))
                    elif row['role'] == 'director':
                        director.append(row['full_name'])
                    last_modified = row['modified']

                film_work_list.append({'_id': film.id,
                                       '_source': FilmWork(director=director,
                                                           actors=actors,
                                                           writers=writers,
                                                           actors_names=[e.name for e in actors],
                                                           writers_names=[e.name for e in writers],
                                                           **film.dict()).dict()})
            logging.info(last_modified)
            result = self.elastic.add(film_work_list)
            if result:
                self.state.set_state('etl', last_modified)


if __name__ == '__main__':
    ETLManager().run()
