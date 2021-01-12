from flask import make_response, render_template
from flask_restful import Resource


class About(Resource):

    def get(self):
        return make_response(render_template("about.html"))
