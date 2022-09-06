import sys
from http import HTTPStatus

import numpy as np
from app.api.db import db
from app.api.model.movie import Movie
from app.api.model.producer import Producer
from flask import Blueprint, jsonify

worst_movie_api = Blueprint("worst_movie_api", __name__)


@worst_movie_api.route("/", methods=["GET"])
def get():
    _winner_producers_more_than_once = (
        db.session.query(Producer.id, db.func.count(Producer.id))
        .join(Movie, Producer.movies)
        .filter(Movie.is_winner == True)
        .group_by(Producer.id)
        .having(db.func.count(Producer.id) > 1)
        .all()
    )

    _winner_movies = (
        db.session.query(Movie.year, Producer.name.label("producer"))
        .join(Producer, Movie.producers)
        .filter(
            Movie.is_winner == True,
            Producer.id.in_([winner.id for winner in _winner_producers_more_than_once]),
        )
        .order_by(Producer.name, Movie.year)
        .all()
    )

    max_producers, min_producers = get_max_min(_winner_movies)

    return (
        jsonify(
            {
                "min": [min.json() for min in min_producers],
                "max": [max.json() for max in max_producers],
            }
        ),
        HTTPStatus.OK,
    )


def get_max_min(_movies):
    producers_with_years = [
        {"producer": x, "years": [y[0] for y in _movies if y[1] == x]}
        for x in set(map(lambda x: x[1], _movies))
    ]
    max_year = 0
    min_year = sys.maxsize
    max_prod = []
    min_prod = []
    for producer in producers_with_years:
        diference = np.diff(producer["years"])
        for i in range(len(diference)):
            if diference[i] > max_year:
                max_prod = [
                    Result(
                        producer["producer"],
                        diference[i],
                        producer["years"][i],
                        producer["years"][i + 1],
                    )
                ]
                max_year = diference[i]

            elif diference[i] == max_year:
                max_prod.append(
                    Result(
                        producer["producer"],
                        diference[i],
                        producer["years"][i],
                        producer["years"][i + 1],
                    )
                )

            if diference[i] < min_year:
                min_prod = [
                    Result(
                        producer["producer"],
                        diference[i],
                        producer["years"][i],
                        producer["years"][i + 1],
                    )
                ]
                min_year = diference[i]
            elif diference[i] == min_year:
                min_prod.append(
                    Result(
                        producer["producer"],
                        diference[i],
                        producer["years"][i],
                        producer["years"][i + 1],
                    )
                )

    return max_prod, min_prod


class Result:
    def __init__(self, producer, interval, previousWin, followingWin) -> None:
        self.producer = producer
        self.interval = int(interval)
        self.previousWin = previousWin
        self.followingWin = followingWin

    def json(self):
        return {
            "producer": self.producer,
            "interval": self.interval,
            "previousWin": self.previousWin,
            "followingWin": self.followingWin,
        }
