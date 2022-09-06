from http import HTTPStatus

from app.api.model.movie import Movie
from app.api.model.producer import Producer


class TestBagHandler:
    @staticmethod
    def test_startup_worst_movie_should_load_csv_on_first_request(test_client):
        response = test_client.get("/worst_movie/")
        count_movie = Movie.query.count()
        count_producer = Producer.query.count()
        assert count_movie == 206
        assert count_producer == 359

    @staticmethod
    def test_get_worst_movie_should_succeed(test_client):
        expected_result = {
            "max": [
                {
                    "followingWin": 2015,
                    "interval": 13,
                    "previousWin": 2002,
                    "producer": "Matthew Vaughn",
                },
                {
                    "followingWin": 2016,
                    "interval": 13,
                    "previousWin": 2003,
                    "producer": "Gerald R. Molen",
                },
            ],
            "min": [
                {
                    "followingWin": 1991,
                    "interval": 1,
                    "previousWin": 1990,
                    "producer": "Joel Silver",
                },
                {
                    "followingWin": 2017,
                    "interval": 1,
                    "previousWin": 2016,
                    "producer": "Gerald R. Molen",
                },
            ],
        }
        response = test_client.get("/worst_movie/")
        response_json = response.get_json()
        assert response.status_code == HTTPStatus.OK

        for expected in expected_result["max"]:
            assert expected in response_json["max"]

        for expected in expected_result["min"]:
            assert expected in response_json["min"]
