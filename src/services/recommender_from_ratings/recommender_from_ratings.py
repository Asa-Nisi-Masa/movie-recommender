from typing import List
import numpy as np
from werkzeug.datastructures import FileStorage

from src.entities import Movie, RecommendedMovies

from src.services.user_ratings_manager import UserRatingsManager
from src.movie_model import MovieModel
from src.services.movie_info_provider import MovieInfoProvider


class RecommenderFromRatings:

    def __init__(
        self,
        user_ratings_manager: UserRatingsManager,
        movie_model: MovieModel,
        movie_info_provider: MovieInfoProvider,
    ):
        self.__user_ratings_manager = user_ratings_manager
        self.__movie_model = movie_model
        self.__movie_info_provider = movie_info_provider

        self.__recommendations_from_ratings_to_retrieve = 15

        # hardcoded user rating mean and standard deviation from the training dataset
        # used to normalize single user ratings
        self.__ratings_mean = 3.533854451353085
        self.__ratings_std = 1.060743961142352

    def get_recommendations_from_ratings(self, file: FileStorage) -> RecommendedMovies:
        user_ids, user_ratings = self.__user_ratings_manager.get_user_movies_and_ratings(file)
        normalized_ratings = self.__get_normalized_ratings(user_ratings)
        recommended_movies = self.__get_recommendations(normalized_ratings, user_ids)

        movies_with_full_info = self.__movie_info_provider.get_movies_with_full_info(recommended_movies)

        return RecommendedMovies(movies_with_full_info)

    def __get_normalized_ratings(self, ratings: np.ndarray) -> np.ndarray:
        return (ratings/2 - self.__ratings_mean) / self.__ratings_std

    def __get_recommendations(self, normalized_ratings: np.ndarray, user_ids: np.ndarray) -> List[Movie]:
        summed = 0
        for rating, id_ in zip(normalized_ratings, user_ids):
            encoding = self.__movie_model.get_movie_by_id(str(id_)).encoding
            weight = rating
            summed += (weight*np.array(encoding))

        num_of_movies_to_fetch = len(normalized_ratings) + self.__recommendations_from_ratings_to_retrieve
        recommendations = self.__movie_model.get_n_closest_movies_by_encoding(list(summed), num_of_movies_to_fetch)
    
        filtered = []
        for movie in recommendations:
            if movie.id_ not in user_ids:
                filtered.append(movie)

                if len(filtered) == self.__recommendations_from_ratings_to_retrieve:
                    return filtered

        raise ValueError("No recommendations")
