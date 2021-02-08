import testing.postgresql
from yoyo import get_backend, read_migrations

from src.services.db_connection_manager import DbConnectionManager
from src.movie_model.movie_model import MovieModel

class TestDbManager:

    def __init__(self, db_connection_manager: DbConnectionManager, movie_model: MovieModel):
        self.__db_connection_manager = db_connection_manager
        self.__movie_model = movie_model
        self.__db_test = None

    def setup_test_db(self) -> None:
        self.__db_test = testing.postgresql.Postgresql()

        self.__db_connection_manager.set_connection(self.__db_test.dsn())
        connection = self.__db_connection_manager.get_connection()
        self.__movie_model.set_connection(connection)

        with connection.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            connection.commit()

        backend = get_backend(self.__db_test.url())
        migrations = read_migrations('./migrations')

        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))

    def teardown_test_db(self) -> None:
        self.__db_test.stop()
