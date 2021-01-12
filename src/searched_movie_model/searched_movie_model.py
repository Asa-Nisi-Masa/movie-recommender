from typing import List
from src.services.db_connection_manager import DbConnectionManager
from src.movie_model import MovieModel
from src.entities import SearchedMovie


class SearchedMovieModel:

    def __init__(self, db_connection_manager: DbConnectionManager, movie_model: MovieModel):
        self.__connection = db_connection_manager.get_connection()
        self.__movie_model = movie_model

    def add_searched_movie(self, title: str, user_id: str) -> None:
        movie = self.__movie_model.get_movie_by_title(title)
        cursor = self.__connection.cursor()
        cursor.execute(
            "INSERT INTO searched_movies (movie_id, user_id) VALUES (%(movie_id)s, %(user_id)s)",
            {
                "movie_id": movie.id_,
                "user_id": user_id,
            }
        )
        self.__connection.commit()

    def get_added_user_movies(self, user_id: str) -> List[SearchedMovie]:
        cursor = self.__connection.cursor()
        cursor.execute(
            "SELECT uuid, movie_id FROM searched_movies WHERE user_id = %(user_id)s",
            {
                "user_id": user_id,
            }
        )

        rows = cursor.fetchall()
        if rows == []:
            return []

        return [
            SearchedMovie(row[0], self.__movie_model.get_movie_by_id(row[1]))
            for row in rows
        ]

    def remove_movie_by_uuid(self, uuid: str) -> None:
        cursor = self.__connection.cursor()
        cursor.execute(
            "DELETE FROM searched_movies WHERE uuid = %(uuid)s",
            {
                "uuid": uuid,
            }
        )
        self.__connection.commit()
