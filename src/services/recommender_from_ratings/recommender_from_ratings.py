from typing import List
import numpy as np
import torch
from werkzeug.datastructures import FileStorage

from src.entities import Movie, RecommendedMovies

from src.services.user_ratings_manager import UserRatingsManager
from src.movie_model import MovieModel
from src.services.user_trainer import UserTrainer
from src.services.movie_info_provider import MovieInfoProvider


class RecommenderFromRatings:

    def __init__(
        self,
        user_ratings_manager: UserRatingsManager,
        movie_model: MovieModel,
        user_trainer: UserTrainer,
        movie_info_provider: MovieInfoProvider,
    ):
        self.__user_ratings_manager = user_ratings_manager
        self.__movie_model = movie_model
        self.__user_trainer = user_trainer
        self.__movie_info_provider = movie_info_provider

        self.__recommendations_from_ratings_to_retrieve = 15

        # hardcoded user rating mean and standard deviation from the training dataset
        # used to normalize single user ratings
        self.__ratings_mean = 3.533854451353085
        self.__ratings_std = 1.060743961142352

    def get_recommendations_from_ratings(self, file: FileStorage) -> RecommendedMovies:
        user_ids, user_ratings = self.__user_ratings_manager.get_user_movies_and_ratings(file)
        normalized_ratings = self.__get_normalized_ratings(user_ratings)

        # -1 because torch weights start at index 0
        predicted_ratings = self.__user_trainer.get_predicted_ratings(user_ids - 1, normalized_ratings)
        recommended_movies = self.__get_recommendations(predicted_ratings, user_ids)
        movies_with_full_info = self.__movie_info_provider.get_movies_with_full_info(recommended_movies)

        return RecommendedMovies(movies_with_full_info)

    def __get_normalized_ratings(self, ratings: torch.Tensor) -> torch.Tensor:
        return (ratings/2 - self.__ratings_mean) / self.__ratings_std

    def __get_recommendations(self, predicted_ratings: torch.Tensor, user_ids: torch.Tensor) -> List[Movie]:
        sorted_predicted_ids = np.argsort(predicted_ratings.cpu().detach().numpy())[0][::-1]    # these ids start at 0

        recommended_movies = []
        for id_ in sorted_predicted_ids:
            id_ = id_ + 1   # +1 because ids in db start at 1
            if id_ not in user_ids:
                movie = self.__movie_model.get_movie_by_id(str(id_))
                recommended_movies.append(movie)

            if len(recommended_movies) == self.__recommendations_from_ratings_to_retrieve:
                return recommended_movies

        raise ValueError("No recommendations")
