from typing import List
from src.entities.movie import Movie


class RecommendedMovies:

    def __init__(self, recommended_movies: List[Movie]):
        self.__recommended_movies = recommended_movies

        self.__index = 0
        self.__index_increment = 5

    @property
    def shown_movies(self) -> List[Movie]:
        low = self.__index
        high = self.__index + self.__index_increment
        return self.__recommended_movies[low:high]

    def increment_up(self) -> None:
        self.__index = min(
            self.__index + self.__index_increment,
            len(self.__recommended_movies) - self.__index_increment
        )

    def increment_down(self) -> None:
        self.__index = max(
            0,
            self.__index - self.__index_increment
        )
