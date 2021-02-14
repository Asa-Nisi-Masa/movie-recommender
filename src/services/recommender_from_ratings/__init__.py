from src.services.user_ratings_manager import user_ratings_manager
from src.movie_model import movie_model
from src.services.user_trainer import user_trainer
from src.services.movie_info_provider import movie_info_provider

from .recommender_from_ratings import RecommenderFromRatings


recommender_from_ratings = RecommenderFromRatings(
    user_ratings_manager,
    movie_model,
    movie_info_provider,
)
