from typing import List
import numpy as np

from src.movie_model import MovieModel
from src.searched_movie_model import SearchedMovieModel
from src.services.movie_info_provider import MovieInfoProvider
from src.entities import Movie, SearchedMovie, RecommendedMovies


class SimilarMovieRecommender:

    def __init__(
        self,
        movie_model: MovieModel,
        searched_movie_model: SearchedMovieModel,
        movie_info_provider: MovieInfoProvider,
    ):
        self.__movie_model = movie_model
        self.__searched_movie_model = searched_movie_model
        self.__movie_info_provider = movie_info_provider

        self.__similar_movies_to_retrieve = 10

    def get_similar_movies(self, searched_movies: List[SearchedMovie]) -> RecommendedMovies:
        # average the movie encodings and find the most similar movies
        if searched_movies == []:
            return []

        encodings = np.array([movie.movie.encoding for movie in searched_movies])
        average_encoding = encodings.mean(axis=0).tolist()

        # we want at least len(movies) movies to prevent possible duplicates
        num_of_movies_to_retrieve = len(searched_movies) + self.__similar_movies_to_retrieve
        similar_movies = self.__movie_model.get_n_closest_movies_by_encoding(average_encoding, num_of_movies_to_retrieve)
        unseen_similar_movies = self.__get_unseen_similar_movies(searched_movies, similar_movies)

        movies_with_full_info = self.__movie_info_provider.get_movies_with_full_info(unseen_similar_movies)
        return RecommendedMovies(movies_with_full_info)

    def get_similar_movie_recommendations(self, title: str) -> List[Movie]:
        return self.__movie_model.get_similar_movies_by_title(title)

    def get_all_movie_titles(self) -> List[str]:
        return self.__movie_model.get_movie_titles()

    def get_added_user_movies(self, user_id: str) -> List[SearchedMovie]:
        return self.__searched_movie_model.get_added_user_movies(user_id)

    def remove_added_user_movie(self, uuid: str) -> None:
        self.__searched_movie_model.remove_movie_by_uuid(uuid)

    def add_searched_movie(self, title: str, user_id: str) -> None:
        self.__searched_movie_model.add_searched_movie(title, user_id)

    def __get_unseen_similar_movies(self, searched_movies: List[Movie], similar_movies: List[Movie]) -> List[Movie]:
        user_entered_titles = [searched_movie.movie.title for searched_movie in searched_movies]
        return [
            movie
            for movie in similar_movies
            if movie.title not in user_entered_titles
        ][:self.__similar_movies_to_retrieve]
