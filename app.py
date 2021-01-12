from dotenv import load_dotenv
load_dotenv()

import uuid
from datetime import timedelta

from flask import Flask
from flask_restful import Api
from flask_session import Session
from flask_dropzone import Dropzone

from src.api.common import Home, About
from src.api.ratings_upload import (
    RatingsUpload,
    RatingsUploadNextMovie,
    RatingsUploadPreviousMovie,
)
from src.api.similar_movie_finder import (
    SearchBar,
    Autocomplete,
    AddSimilarMovie,
    SimilarMovieFinder,
    RemoveSimilarMovie,
    SimilarMovieFinderNext,
    SimilarMovieFinderPrevious,
)


app = Flask(__name__, template_folder="./templates/", static_folder="./styles/")
app.config.update(
    {
        "DROPZONE_ALLOWED_FILE_CUSTOM": True,
        "DROPZONE_ALLOWED_FILE_TYPE": ".csv",
        "DROPZONE_DEFAULT_MESSAGE": "Drag & drop or select your movie ratings",
        "DROPZONE_MAX_FILES": 1,
        "DROPZONE_MAX_FILE_SIZE": 10,
        "DROPZONE_REDIRECT_VIEW": "ratingsupload",
        "PERMANENT_SESSION_LIFETIME": timedelta(minutes=10),
        "SECRET_KEY": uuid.uuid4().hex,
        "SESSION_TYPE": "filesystem",
    }
)

Dropzone(app)
Session(app)
api = Api(app)


api.add_resource(Home, "/")
api.add_resource(About, "/about")
api.add_resource(SearchBar, "/search-bar")
api.add_resource(Autocomplete, "/_autocomplete")
api.add_resource(RatingsUpload, "/ratings-upload")
api.add_resource(AddSimilarMovie, "/add-similar-movie")
api.add_resource(SimilarMovieFinder, "/similar-movie-finder")
api.add_resource(RemoveSimilarMovie, "/remove-similar-movie/<uuid_>")
api.add_resource(RatingsUploadNextMovie, "/ratings-upload-next-movie")
api.add_resource(SimilarMovieFinderNext, "/similar-movie-finder-next")
api.add_resource(RatingsUploadPreviousMovie, "/ratings-upload-previous-movie")
api.add_resource(SimilarMovieFinderPrevious, "/similar-movie-finder-previous")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
