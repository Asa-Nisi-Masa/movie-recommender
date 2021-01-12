from src.services.db_connection_manager import db_connection_manager
from src.movie_model import movie_model
from .searched_movie_model import SearchedMovieModel


searched_movie_model = SearchedMovieModel(db_connection_manager, movie_model)
