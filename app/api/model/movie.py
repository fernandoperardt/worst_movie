from app.api.db import db

movie_producer = db.Table(
    "movie_producer",
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id")),
    db.Column("producer_id", db.Integer, db.ForeignKey("producers.id")),
)


class Movie(db.Model):
    __tablename__ = "movies"

    def __init__(self, year: int, title: str, is_winner: bool) -> None:
        self.year = year
        self.title = title
        self.is_winner = is_winner

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    title = db.Column(db.String(255))
    is_winner = db.Column(db.Boolean, index=True)
    producers = db.relationship("Producer", secondary=movie_producer)
