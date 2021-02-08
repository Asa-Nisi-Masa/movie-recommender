from typing import Optional
from src.movie_model import MovieModel


class Mapper:

    def __init__(self, movie_model: MovieModel):
        self.__movie_model = movie_model
        self.__imdb_id_to_id_mapper = self.__get_imdb_to_id_map()

    def map_imdb_id_to_id(self, imdb_id: str) -> Optional[str]:
        try:
            return self.__imdb_id_to_id_mapper[imdb_id]
        except KeyError:
            return

    def __get_imdb_to_id_map(self) -> Optional[dict]:
        try:
            return dict(self.__movie_model.get_imdb_ids_and_ids())
        except AttributeError:
            return
