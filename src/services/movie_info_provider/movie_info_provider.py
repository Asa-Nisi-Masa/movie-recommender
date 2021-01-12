import os
from typing import List
import aiohttp
import asyncio

from src.entities import Movie


class MovieInfoProvider:
    """
    Provides additional data from the movie API so that there is no need to store all of the movie data in the database
    """

    def __init__(self):
        self.__max_genres_to_show = 2

    def get_movies_with_full_info(self, movies: List[Movie]) -> List[Movie]:
        full_data = asyncio.run(self.__collect_full_data_of_movies(movies))

        full_info_movies = []
        for movie, api_info in zip(movies, full_data):
            movie_full = Movie(
                id_=movie.id_,
                imdb_id=movie.imdb_id,
                title=self.__get_movie_property(api_info, "Title"),
                genres=self.__get_genres(api_info),
                year=self.__get_movie_property(api_info, "Year"),
                encoding=movie.encoding,
                hyperlink=movie.hyperlink,
                poster=api_info["Poster"],
            )
            full_info_movies.append(movie_full)

        return full_info_movies

    async def __collect_full_data_of_movies(self, movies: List[Movie]) -> List[dict]:
        urls = [
            f"http://www.omdbapi.com/?i={movie.imdb_id}&apikey={os.environ.get('MOVIE_API_KEY')}"
            for movie in movies
        ]
        return await asyncio.gather(*[self.__get_single_movie_data(url) for url in urls])

    async def __get_single_movie_data(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as response:
                return await response.json()

    def __get_movie_property(self, api_info: dict, key: str) -> str:
        value = api_info[key]
        if value == "N/A":
            return ""

        return value

    def __get_genres(self, api_info: dict) -> str:
        genres = self.__get_movie_property(api_info, "Genre")
        genres_separate = genres.split(", ")[:self.__max_genres_to_show]
        return ", ".join(genres_separate)
