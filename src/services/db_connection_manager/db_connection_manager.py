import os
from typing import Optional
import psycopg2
# import testing.postgresql
from src.services.test_db_manager import test_db_manager


class DbConnectionManager:

    def __init__(self):
        self.__connection = None
        dsn = {
            "host": os.environ.get("DB_HOST"),
            "dbname": os.environ.get("DB_NAME"),
            "user": os.environ.get("DB_USER"),
            "password": os.environ.get("DB_PASSWORD"),
        }
        self.set_connection(dsn)

    def get_connection(self) -> Optional[psycopg2.extensions.connection]:
        return self.__connection

    def set_connection(self, dsn: dict) -> None:
        try:
            self.__connection = psycopg2.connect(**dsn)
        except psycopg2.OperationalError:
            self.__connection = test_db_manager.get_test_connection()
