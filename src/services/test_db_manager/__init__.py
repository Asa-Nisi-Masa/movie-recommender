from src.services.db_connection_manager import db_connection_manager
from src.movie_model import movie_model
from .test_db_manager import TestDbManager


test_db_manager = TestDbManager(db_connection_manager, movie_model)
