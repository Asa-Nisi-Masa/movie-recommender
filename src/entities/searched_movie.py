from src.entities.movie import Movie


class SearchedMovie:

    __slots__ = ("__uuid", "__movie")

    def __init__(self, uuid: str, movie: Movie):
        self.__uuid = uuid
        self.__movie = movie

    def __str__(self) -> str:
        return f"SearchedMovie(id={self.__movie.id_}, imdb_id={self.__movie.imdb_id}, title={self.__movie.title}"

    def __repr__(self) -> str:
        return self.__str__

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def movie(self) -> Movie:
        return self.__movie
