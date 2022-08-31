from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from resources.worst_movie import worst_movie_api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.register_blueprint(worst_movie_api, url_prefix="/worst_movie")

if __name__ == '__main__':
    app.run(port = 5000, debug = True)