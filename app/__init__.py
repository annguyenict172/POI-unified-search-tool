from flask import Flask, jsonify
from marshmallow import Schema, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from app.decorators import parse_args_with

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import *
from app.api_dispatcher import APIDispatcher
from app import parameter_parser
from app.data_aggregator import DataAggregator
from app.data_preprocessor import DataPreprocessor
from app.cache import get_cache_with_key, set_cache_with_key


class FindPlaceSchema(Schema):
    location = fields.String(required=True)
    keyword = fields.String(missing=None)
    radius = fields.Integer(missing=None)
    categories = fields.String(missing=None)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    arguments = parameter_parser.parse_parameters(raw_params=args)
    cache_results = get_cache_with_key(args['location'])
    if cache_results is None:
        responses = APIDispatcher(args=arguments).dispatch_api_calls()
        preprocessed_data = DataPreprocessor(data=responses).process_data()
        results = DataAggregator(data=preprocessed_data).aggregate_data()
        set_cache_with_key(args['location'], results)
    else:
        results = []
        categories = args.get('categories').split(',') if args.get('categories') else []
        counts = {}
        for category in categories:
            counts[category] = 0
        for category in categories:
            gg_cat = Category.query.filter_by(service='google', text=category).first().service_identifier
            fb_cat = Category.query.filter_by(service='facebook', text=category).first().service_identifier
            fs_cat = Category.query.filter_by(service='foursquare', text=category).first().service_identifier
            for item in cache_results:
                if item.get('facebook') and item['facebook']['unified_type'] == fb_cat:
                    counts[category] += 1
                    results.append(item)
                elif item.get('google') and item['google']['unified_type'] == gg_cat:
                    counts[category] += 1
                    results.append(item)
                elif item.get('foursquare') and item['foursquare']['unified_type'] == fs_cat:
                    counts[category] += 1
                    results.append(item)
        remaining_categories = []
        for category in categories:
            if counts[category] == 0:
                remaining_categories.append(category)
        print(counts)
        if len(remaining_categories) > 0:
            args['categories'] = ','.join(remaining_categories)
            arguments = parameter_parser.parse_parameters(raw_params=args)
            responses = APIDispatcher(args=arguments).dispatch_api_calls()
            preprocessed_data = DataPreprocessor(data=responses).process_data()
            results.extend(DataAggregator(data=preprocessed_data).aggregate_data())
            set_cache_with_key(args['location'], results)

    return jsonify(results)
