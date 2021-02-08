import testing.postgresql
import psycopg2
from yoyo import get_backend, read_migrations


class TestDbManager:

    def __init__(self):
        self.__postgres = None
        self.__connection = None
        self.setup_test_db()

    def setup_test_db(self) -> None:
        self.__postgres = testing.postgresql.Postgresql()
        self.__connection = psycopg2.connect(**self.__postgres.dsn())

        with self.__connection.cursor() as cursor:
            cursor.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            self.__connection.commit()

        backend = get_backend(self.__postgres.url())
        migrations = read_migrations('./migrations')

        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))

    def teardown_test_db(self) -> None:
        self.__postgres.stop()

    def get_test_connection(self) -> psycopg2.extensions.connection:
        return self.__connection
