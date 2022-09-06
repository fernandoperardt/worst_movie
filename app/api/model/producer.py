from app.api.db import db
from app.api.model.movie import movie_producer


class Producer(db.Model):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    movies = db.relationship("Movie", secondary=movie_producer, overlaps="producers")

    def __init__(self, name) -> None:
        self.name = name

    @classmethod
    def get_or_create_producer(cls, _name):
        _producer = cls.query.filter_by(name=_name).first()
        if not _producer:
            _producer = cls(_name)
            db.session.add(_producer)
        return _producer
