from . import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(500), unique=True, nullable=False)