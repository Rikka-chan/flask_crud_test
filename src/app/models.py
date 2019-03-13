import datetime

from app import db


class Book(db.Model):
    """This class represents the book table."""

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    date_finished = db.Column(db.Date, default=db.func.current_timestamp())
    rank = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    def __init__(self, name, author, rank, date_finished=datetime.datetime.now()):
        """initialize with name."""
        self.name = name
        self.author = author
        self.rank = rank
        self.date_finished = date_finished

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Book.query.filter_by(deleted=False)

    def delete(self):
        self.deleted = True
        db.session.commit()

    def __repr__(self):
        return "<Book: {}>".format(self.name)
