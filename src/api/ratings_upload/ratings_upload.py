from flask_restful import Resource
from flask import request, render_template, make_response, session

from src.services.recommender_from_ratings import recommender_from_ratings
from src.movie_exception import MovieException


class RatingsUpload(Resource):

    def get(self):
        recommended_movies = session.get("movies")
        error = session.get("error")

        return make_response(render_template("upload.html", movies=recommended_movies, error=error))

    def post(self):
        try:
            recommended_movies = recommender_from_ratings.get_recommendations_from_ratings(request.files["file"])
            session["error"] = None
            session["movies"] = recommended_movies
        except MovieException as error:
            session["error"] = str(error)
            session["movies"] = None

            return {"error": error.code}, 400

        return "", 204
