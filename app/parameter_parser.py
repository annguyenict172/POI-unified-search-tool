from app.models import Term
from app.constants import Provider


def parse_parameters(raw_params):
    formatted_params = {}
    for provider in Provider.get_list():
        formatted_params[provider] = {}
        for key, val in raw_params.items():
            if key == 'categories':
                value = _find_matched_categories(val.split(','), provider)
            else:
                value = val
            formatted_key = Term.query.filter_by(term=key, provider=provider).first().matched_term
            formatted_params[provider][formatted_key] = value

    return formatted_params


def _find_matched_categories(categories, provider):
    matched_categories = set()
    for category in categories:
        term = Term.query.filter_by(term=category, provider=provider).first().matched_term
        matched_categories.add(term)
    return matched_categories
