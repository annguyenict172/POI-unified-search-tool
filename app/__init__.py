from flask import Flask, jsonify
from marshmallow import Schema, fields
import requests

from config import Config
from app.helper import parse_args_with
from app.constant import FoursquareEndpoint, GoogleEndpoint

app = Flask(__name__)
app.config.from_object(Config)


class FindPlaceSchema(Schema):
    query = fields.String(required=True)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    response = requests.get(GoogleEndpoint.FREE_TEXT_SEARCH, params={
        'query': args['query'],
        'key': Config.GOOGLE_PLACE_API_KEY
    })
    return jsonify(response.json())
