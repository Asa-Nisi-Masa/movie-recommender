from flask import redirect, url_for
from flask_restful import Resource


class Home(Resource):

    def get(self):
        return redirect(url_for("similarmoviefinder"))
