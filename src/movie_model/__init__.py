from .movie_model import MovieModel
from src.services.db_connection_manager import db_connection_manager


movie_model = MovieModel(db_connection_manager)
