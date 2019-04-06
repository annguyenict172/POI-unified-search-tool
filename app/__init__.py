from flask import Flask, jsonify
from marshmallow import Schema, fields
from flask_cors import CORS

from config import Config
from app.helper import parse_args_with
from app.api import GooglePlaceAPI, FoursquareAPI

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
google_api = GooglePlaceAPI()
foursquare_api = FoursquareAPI()


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
