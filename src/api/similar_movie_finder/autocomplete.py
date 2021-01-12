import json
from flask import Response
from flask_restful import Resource

from src.services.similar_movie_recommender import similar_movie_recommender


class Autocomplete(Resource):

    def __init__(self):
        self.__movie_titles = similar_movie_recommender.get_all_movie_titles()

    def get(self):
        return Response(json.dumps(self.__movie_titles), mimetype='application/json')
