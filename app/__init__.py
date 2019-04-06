from flask import Flask, jsonify
from marshmallow import Schema, fields

from config import Config
from app.helper import parse_args_with
from app.api import GooglePlaceAPI, FoursquareAPI

app = Flask(__name__)
app.config.from_object(Config)
google_api = GooglePlaceAPI()
foursquare_api = FoursquareAPI()


class FindPlaceSchema(Schema):
    query = fields.String(required=True)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    response = google_api.freetext_search(params=args)
    return jsonify(response.json())
