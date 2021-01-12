from flask import redirect, url_for
from flask_restful import Resource

from src.services.similar_movie_recommender import similar_movie_recommender


class RemoveSimilarMovie(Resource):

    def get(self, uuid_: str):
        similar_movie_recommender.remove_added_user_movie(uuid_)
        return redirect(url_for("similarmoviefinder"))
