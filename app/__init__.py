from flask import Flask, jsonify
from marshmallow import Schema, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from app.decorators import parse_args_with
from libs.cache import retrieve_from_cache, store_to_cache

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


class FindPlaceSchema(Schema):
    location = fields.String(required=True)
    keyword = fields.String(missing=None)
    radius = fields.Float(missing=1)
    categories = fields.String(missing=None)
    page = fields.Integer(missing=None)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    keyword = args.get('keyword')
    if not keyword:
        results, page, total_pages = retrieve_from_cache(args)
        if results is not None:
            return jsonify({
                'results': results,
                'page': page,
                'total_pages': total_pages,
            })
    arguments = parameter_parser.parse_parameters(raw_params=args)
    responses = APIDispatcher(args=arguments).dispatch_api_calls()
    preprocessed_data = DataPreprocessor(data=responses).process_data()
    results = DataAggregator(data=preprocessed_data).aggregate_data()

    if not keyword and len(results) > 0:
        first_page_results, total_pages = store_to_cache(args, results)
        if first_page_results is not None:
            return jsonify({
                'results': first_page_results,
                'page': 1,
                'total_pages': total_pages,
            })

    return jsonify({
        'results': results,
        'page': 1,
        'total_pages': 1,
    })
