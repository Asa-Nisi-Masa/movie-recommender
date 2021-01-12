from flask import request, render_template, make_response, session
from flask_restful import Resource

from src.api.similar_movie_finder.search_form import SearchForm
from src.services.similar_movie_recommender import similar_movie_recommender


class SimilarMovieFinder(Resource):

    def get(self):
        cookie = request.cookies
        form = SearchForm(request.form)
        error = request.args.get("error")
        user_id = cookie.get("user_id")
        similar_movies = None

        if "search-submit-button" in request.args:
            user_added_movies = similar_movie_recommender.get_added_user_movies(user_id)
            similar_movies = similar_movie_recommender.get_similar_movies(user_added_movies)
            session["similar_movies"] = similar_movies

        user_added_movies = similar_movie_recommender.get_added_user_movies(user_id)

        return make_response(
            render_template(
                "similar_movie.html",
                form=form,
                error=error,
                user_added_movies=user_added_movies,
                movies=similar_movies
            )
        )
