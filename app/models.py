from app import db


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    raw_text = db.Column(db.String(length=250), nullable=False)
    formatted_text = db.Column(db.String(length=200), nullable=False)
    service = db.Column(db.String(length=20), nullable=False)
    service_identifier = db.Column(db.String(length=250), nullable=False)
