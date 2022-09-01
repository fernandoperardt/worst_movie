import csv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.api.resources.worst_movie import worst_movie_api
from app.api.db import config_db

def create_app():
    _app = Flask(__name__)
    config_db(_app)

    _app.register_blueprint(worst_movie_api, url_prefix="/worst_movie")

    load_database_from_csv()

    return _app


def load_database_from_csv():
    with open('app/pre_load.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            print(row['year'], row['producers'], ' - winer: ',  row['winner'])

if __name__ == '__main__':
    app = create_app()
    app.run(port = 5000, debug = True)