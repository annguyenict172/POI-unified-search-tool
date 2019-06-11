import requests
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
from app.parameter_parser import ParametersParser
from app.result_aggregator import ResultAggregator
from app.response_formatter import ResponseFormatter
from app.cache import Cache
from app.cache_result_filter import CacheResultFilter
from app.constants import Provider


MINIMUM_NUM_OF_PROVIDERS = 3


class ItemSchema(Schema):
    name = fields.String()
    lat = fields.Float()
    lng = fields.Float()
    provider = fields.String()


class MergedSchema(Schema):
    facebook = fields.Nested(ItemSchema())
    google = fields.Nested(ItemSchema())
    foursquare = fields.Nested(ItemSchema())


class FindPlaceSchema(Schema):
    location = fields.String(required=True)
    keyword = fields.String(missing=None)
    radius = fields.Integer(missing=None)
    categories = fields.String(missing=None)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    parameters = ParametersParser(parameters=args).parse_parameters()
    cache_results = Cache.get_from_location(args['location'])
    if cache_results is None:
        # Dispatch API calls
        responses = APIDispatcher(parameters=parameters).dispatch_api_calls()
        # Format the responses from multiple providers to a consistent format
        formatted_responses = ResponseFormatter(raw_responses=responses).format_responses()
        # Save the formatted results into cache
        Cache.set_cache_with_location(args['location'], formatted_responses)
        # Aggregate the final results
        results = ResultAggregator(data=formatted_responses).aggregate_results()
    else:
        # Filter the cache results. If the cache results do not satisfy all search parameters,
        # we will continue to make API calls using the search parameters which were not satisfied
        results, remaining_categories = CacheResultFilter.filter_cache_results(args, cache_results)
        if len(remaining_categories) != 0 or len(results) == 0:
            if len(remaining_categories) != 0:
                args['categories'] = ','.join(remaining_categories)
            parameters = ParametersParser(parameters=args).parse_parameters()
            # Dispatch API calls
            responses = APIDispatcher(parameters=parameters).dispatch_api_calls()
            # Format the responses from multiple providers to a consistent format
            formatted_responses = ResponseFormatter(raw_responses=responses).format_responses()
            # Extend the cache results and save them
            cache_results.extend(formatted_responses)
            Cache.set_cache_with_location(args['location'], cache_results)
            # Aggregate the final results
            results.extend(formatted_responses)
            results = ResultAggregator(data=results).aggregate_results()
        else:
            # Aggregate the final results
            results = ResultAggregator(data=results).aggregate_results()

    limited_results = []
    for item in results:
        if len(item.keys()) >= MINIMUM_NUM_OF_PROVIDERS:
            limited_results.append(item)

    return jsonify({
        'statistic': calculate_results_statistic(results),
        'results': limited_results
    })


def calculate_results_statistic(results):
    statistic = {
        Provider.GOOGLE: 0,
        Provider.FACEBOOK: 0,
        Provider.FOURSQUARE: 0,
        '1': 0,
        '2': 0,
        '3': 0
    }
    for item in results:
        if item.get(Provider.FOURSQUARE):
            statistic[Provider.FOURSQUARE] += 1
        if item.get(Provider.FACEBOOK):
            statistic[Provider.FACEBOOK] += 1
        if item.get(Provider.GOOGLE):
            statistic[Provider.GOOGLE] += 1
        statistic[str(len(item.keys()))] += 1
    return statistic


class GoogleDetail(Schema):
    place_id = fields.String(required=True)


@app.route('/google/details')
@parse_args_with(GoogleDetail)
def get_google_detail(args):
    res = requests.get('https://maps.googleapis.com/maps/api/place/details/json', params={
        'placeid': args['place_id'],
        'key': Config.GOOGLE_PLACE_API_KEY
    })
    return jsonify(res.json())


class GooglePhoto(Schema):
    photo_reference = fields.String(required=True)


@app.route('/google/photo')
@parse_args_with(GooglePhoto)
def get_google_photo(args):
    res = requests.get('https://maps.googleapis.com/maps/api/place/photo', params={
        'maxwidth': 400,
        'photoreference': args['photo_reference'],
        'key': Config.GOOGLE_PLACE_API_KEY
    })
    return jsonify({'link': res.url})
