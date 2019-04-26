from app import db


class Category(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.String(length=100))
    service = db.Column(db.String(length=20))
    service_identifier = db.Column(db.String(length=100))
