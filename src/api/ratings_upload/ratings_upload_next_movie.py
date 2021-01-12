from flask import session, render_template, make_response
from flask_restful import Resource


class RatingsUploadNextMovie(Resource):

    def get(self):
        recommended_movies = None
        if "movies" in session:
            recommended_movies = session.get("movies")
            recommended_movies.increment_up()

        return make_response(render_template("movie.html", movies=recommended_movies))
