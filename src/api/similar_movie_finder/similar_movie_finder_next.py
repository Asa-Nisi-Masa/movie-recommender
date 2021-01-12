from flask import session, make_response, render_template
from flask_restful import Resource


class SimilarMovieFinderNext(Resource):

    def get(self):
        similar_movies = None
        if "similar_movies" in session:
            similar_movies = session.get("similar_movies")
            similar_movies.increment_up()

        return make_response(render_template("movie.html", movies=similar_movies))
