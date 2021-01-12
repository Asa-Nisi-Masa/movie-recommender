from typing import Optional
from src.movie_model import MovieModel


class Mapper:

    def __init__(self, movie_model: MovieModel):
        self.__imdb_id_to_id_mapper = dict(movie_model.get_imdb_ids_and_ids())

    def map_imdb_id_to_id(self, imdb_id: str) -> Optional[str]:
        try:
            return self.__imdb_id_to_id_mapper[imdb_id]
        except KeyError:
            return
