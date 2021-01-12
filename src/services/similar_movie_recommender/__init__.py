from src.movie_model import movie_model
from src.searched_movie_model import searched_movie_model
from src.services.movie_info_provider import movie_info_provider

from .similar_movie_recommender import SimilarMovieRecommender


similar_movie_recommender = SimilarMovieRecommender(movie_model, searched_movie_model, movie_info_provider)
