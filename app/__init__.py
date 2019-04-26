from difflib import SequenceMatcher

from flask import Flask, jsonify
from marshmallow import Schema, fields
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from app.helper import parse_args_with

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import *
from app.query_dispatcher import QueryDispatcher
from app import argument_extractor


class FindPlaceSchema(Schema):
    query = fields.String(required=True)


@app.route('/places/explore')
@parse_args_with(FindPlaceSchema)
def explore_places(args):
    arguments = argument_extractor.extract_arguments(args['query'])
    query_dispatcher = QueryDispatcher(args=arguments)
    responses = query_dispatcher.dispatch_explore_query()
    return jsonify(responses)
