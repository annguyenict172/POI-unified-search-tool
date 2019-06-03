from app import db


class Term(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    term = db.Column(db.String(length=20))
    provider = db.Column(db.String(length=20))
    matched_term = db.Column(db.String(length=20))
