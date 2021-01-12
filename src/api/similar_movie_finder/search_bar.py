import uuid
from flask import request, redirect, url_for
from flask_restful import Resource


class SearchBar(Resource):

    def get(self):
        movie_search_bar = request.args.get("search_autocomplete")

        if "search-add-button" in request.args:
            response = redirect(url_for("addsimilarmovie", movie_to_add=movie_search_bar))

            cookie_user_id = request.cookies.get("user_id")
            if cookie_user_id is None:
                user_id = uuid.uuid4().hex
                response.set_cookie("user_id", user_id)

            return response

        return redirect(url_for("similarmoviefinder"))
