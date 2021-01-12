from typing import Tuple
import pandas as pd
from pandas.errors import EmptyDataError
import torch
import numpy as np
from werkzeug.datastructures import FileStorage

from src.services.mapper import Mapper
from src.movie_exception import MovieException


class UserRatingsManager:

    def __init__(self, mapper: Mapper):
        self.__mapper = mapper

    def get_user_movies_and_ratings(self, file: FileStorage) -> Tuple[torch.Tensor, torch.Tensor]:
        data_frame = self.__get_valid_data_frame(file)
        raw_imdb_ids = self.__get_valid_imdb_ids(data_frame)
        raw_ratings = self.__get_valid_ratings(data_frame)

        return self.__get_ids_and_ratings(raw_imdb_ids, raw_ratings)

    def __get_valid_data_frame(self, file: FileStorage) -> pd.DataFrame:
        try:
            data_frame = pd.read_csv(file, encoding="latin-1")
        except EmptyDataError:
            raise MovieException(
                MovieException.error_empty_file_attached,
                "Empty/incorrectly formatted .csv. Check the 'About' page for more info",
            )

        return data_frame.dropna()

    def __get_valid_imdb_ids(self, data_frame: pd.DataFrame) -> np.ndarray:
        try:
            return data_frame["Const"].values
        except KeyError:
            try:
                return data_frame["IMDbId"].values
            except KeyError:
                raise MovieException(
                    MovieException.error_data_frame_missing_key,
                    "Incorrectly formatted .csv file. Missing 'Const'/'IMDbId' column!",
                )

    def __get_valid_ratings(self, data_frame: pd.DataFrame) -> np.ndarray:
        try:
            return data_frame["Your Rating"].values
        except KeyError:
            raise MovieException(
                MovieException.error_data_frame_missing_key,
                "Incorrectly formatted .csv file. Missing 'Your Rating' column!"
            )

    def __get_ids_and_ratings(
        self, raw_imdb_ids: np.ndarray, raw_ratings: np.ndarray
    ) -> Tuple[torch.Tensor, torch.Tensor]:

        ids = []
        ratings = []
        for imdb_id, raw_rating in zip(raw_imdb_ids, raw_ratings):
            id_ = self.__mapper.map_imdb_id_to_id(imdb_id)
            if id_ is not None:
                ids.append(id_)
                ratings.append(raw_rating)

        return torch.tensor(ids).long(), torch.tensor(ratings).long()
