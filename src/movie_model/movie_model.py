from typing import List
import torch

from src.services.db_connection_manager import DbConnectionManager
from src.entities import Movie
from src.movie_exception import MovieException


class MovieModel:

    def __init__(self, db_connection_manager: DbConnectionManager):
        self.__connection = db_connection_manager.get_connection()

    def get_imdb_ids_and_ids(self) -> list:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT imdb_id, id FROM movies")
        return cursor.fetchall()

    def get_movie_by_id(self, id_: str) -> Movie:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT * FROM movies WHERE id = %(id)s",
            {
                "id": id_,
            }
        )
        row = cursor.fetchone()

        return Movie(*row)

    def get_number_of_movies(self) -> int:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM movies")
        return cursor.fetchone()[0]

    def get_number_of_users(self) -> int:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        return cursor.fetchone()[0]

    def get_movie_titles(self) -> List[str]:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT title FROM movies")
        titles = cursor.fetchall()
        return list(list(zip(*titles))[0])

    def get_similar_movies_by_title(self, title: str) -> List[Movie]:
        cursor = self.__connection.cursor()
        movie_of_interest = self.get_movie_by_title(title)

        cursor.execute(
            "SELECT * FROM movies ORDER BY cosine_sim(%(encoding_of_interest)s, encoding) DESC LIMIT 5",
            {
                "encoding_of_interest": movie_of_interest.encoding,
            }
        )
        rows = cursor.fetchall()
        return [Movie(*row) for row in rows]

    def get_movie_by_title(self, title: str) -> Movie:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT * FROM movies WHERE title = %(title)s",
            {
                "title": title,
            }
        )
        row = cursor.fetchone()

        if row is not None:
            return Movie(*row)

        raise MovieException(
            MovieException.error_no_movie_found_by_title,
            "No matching movies found"
        )

    def get_n_closest_movies_by_encoding(self, encoding: List[float], number_of_movies: int) -> List[Movie]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT * FROM movies ORDER BY cosine_sim(%(encoding)s, encoding) DESC LIMIT %(limit)s",
            {
                "encoding": encoding,
                "limit": number_of_movies,
            }
        )
        rows = cursor.fetchall()
        return [Movie(*row) for row in rows]

    def get_movie_encodings(self) -> torch.Tensor:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT encoding FROM movies")

        rows = cursor.fetchall()
        if rows == []:
            return torch.tensor([])

        return torch.tensor(rows)[:, 0, :]

    def get_user_encodings(self) -> torch.Tensor:
        cursor = self.__connection.cursor()
        cursor.execute("SELECT encoding FROM users")

        rows = cursor.fetchall()
        if rows == []:
            return torch.tensor([])

        return torch.tensor(rows)[:, 0, :]
