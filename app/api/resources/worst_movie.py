from flask import Blueprint
from http import HTTPStatus

worst_movie_api = Blueprint("worst_movie_api", __name__)

@worst_movie_api.route("/", methods=["GET"])
def get():
    return {'teste': 'ok'}, HTTPStatus.OK