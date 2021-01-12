from flask import session, render_template, make_response
from flask_restful import Resource


class RatingsUploadPreviousMovie(Resource):

    def get(self):
        recommended_movies = None
        if "movies" in session:
            recommended_movies = session.get("movies")
            recommended_movies.increment_down()

        return make_response(render_template("movie.html", movies=recommended_movies))
