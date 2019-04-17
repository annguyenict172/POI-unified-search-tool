from flask import Flask, jsonify
from marshmallow import Schema, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from app.helper import parse_args_with
from app.api import GooglePlaceAPI, FoursquareAPI

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
google_api = GooglePlaceAPI()
foursquare_api = FoursquareAPI()

from app.models import *


class FindPlaceSchema(Schema):
    query = fields.String(missing=None)
    lat = fields.Float(required=True)
    long = fields.Float(required=True)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    places = google_api.nearby_search(params={
        'location': '{},{}'.format(args['lat'], args['long']),
        'radius': 2000,
        'keyword': args['query']
    }) + foursquare_api.search_venues(params={
        'll': '{},{}'.format(args['lat'], args['long']),
        'radius': 2000,
        'limit': 10,
        'query': args['query']
    })
    return jsonify(places)
