import csv

from flask import Flask

from app.api.db import config_db, db
from app.api.model.movie import Movie
from app.api.model.producer import Producer
from app.api.resources.worst_movie import worst_movie_api
from app.api.utils import split_producer_names


def create_app():
    app = Flask(__name__)

    config_db(app)

    app.register_blueprint(worst_movie_api, url_prefix="/worst_movie")

    @app.before_first_request
    def before_first_request():
        clear_data(db.session)
        with app.app_context():
            __load_database_from_csv()

    return app


def clear_data(session):
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()


def __load_database_from_csv():
    with open("app/pre_load.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for movie_row in reader:
            movie = Movie(
                movie_row["year"], movie_row["title"], movie_row["winner"] == "yes"
            )
            producers = []
            for producer_name in split_producer_names(movie_row["producers"]):
                producers.append(Producer.get_or_create_producer(producer_name))
            movie.producers = producers
            db.session.add(movie)
            db.session.commit()


if __name__ == "__main__":
    app = create_app()

    app.run(port=5000, debug=True)
