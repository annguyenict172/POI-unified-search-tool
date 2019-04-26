from functools import wraps

from flask import request, jsonify


def parse_args_with(schema):
    def parse_args_with_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request_args = request.get_json() or {}
            if request.method == 'GET':
                request_args = request.args.to_dict()
            parsed_args, args_errors = schema().load(request_args)
            if args_errors:
                return jsonify(args_errors), 400
            kwargs['args'] = parsed_args
            return f(*args, **kwargs)

        return decorated_function

    return parse_args_with_decorator
