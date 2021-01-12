from flask import request, redirect, url_for
from flask_restful import Resource

from src.movie_exception import MovieException
from src.services.similar_movie_recommender import similar_movie_recommender


class AddSimilarMovie(Resource):

    def get(self):
        cookie = request.cookies
        movie_to_add = request.args.get("movie_to_add")

        user_id = cookie.get("user_id")
        try:
            similar_movie_recommender.add_searched_movie(movie_to_add, user_id)
        except MovieException as error:
            return redirect(url_for("similarmoviefinder", error=str(error)))

        return redirect(url_for("similarmoviefinder"))
