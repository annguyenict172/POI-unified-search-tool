from difflib import SequenceMatcher

from flask import Flask, jsonify
from marshmallow import Schema, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from app.helper import parse_args_with
from app import argument_extractor

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import *
from app.query_dispatcher import QueryDispatcher


class FindPlaceSchema(Schema):
    query = fields.String(required=True)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    arguments = argument_extractor.extract_arguments(args['query'])
    query_dispatcher = QueryDispatcher(args=arguments)
    results = query_dispatcher.dispatch_query()
    return jsonify(results)
    # matched = []
    # for i, item in enumerate(results):
    #     if i == 0:
    #         continue
    #     else:
    #         distance = compare_distance(results[i-1], item)
    #         name_similar = similar(results[i-1]['core_info']['name'], item['core_info']['name'])
    #         if distance < 100 and name_similar > 0.4:
    #             print(results[i - 1]['core_info']['name'])
    #             print(item['core_info']['name'])
    #             matched.append({
    #                 **results[i-1],
    #                 **item
    #             })
    # return jsonify(matched)


def compare_distance(item1, item2):
    from math import sin, cos, sqrt, atan2, radians

    lat1 = radians(item1['core_info']['location']['lat'])
    lng1 = radians(item1['core_info']['location']['lng'])
    lat2 = radians(item2['core_info']['location']['lat'])
    lng2 = radians(item2['core_info']['location']['lng'])

    # approximate radius of earth in km
    R = 6373.0

    dlon = lng2 - lng1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance * 1000


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
