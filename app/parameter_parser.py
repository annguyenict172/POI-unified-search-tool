from app.models import Category
from app.constants import Service


def parse_parameters(raw_params):
    categories = raw_params.get('categories').split(',') if raw_params.get('categories') else []
    formatted_params = {
        Service.GOOGLE: {
            'location': raw_params.get('location'),
            'radius': raw_params.get('radius'),
            'types': _find_matched_categories(categories, Service.GOOGLE),
            'keyword': raw_params.get('keyword')
        },
        Service.FACEBOOK: {
            'center': raw_params.get('location'),
            'distance': raw_params.get('radius'),
            'categories': _find_matched_categories(categories, Service.FACEBOOK),
            'q': raw_params.get('keyword')
        },
        Service.FOURSQUARE: {
            'll': raw_params.get('location'),
            'radius': raw_params.get('radius'),
            'sections': _find_matched_categories(categories, Service.FOURSQUARE),
            'query': raw_params.get('keyword')
        }
    }
    return formatted_params


def _find_matched_categories(terms, service):
    types = set()
    for term in terms:
        categories = Category.query.filter(
            Category.service == service,
            Category.text.like('%{}%'.format(term))
        ).all()
        for category in categories:
            types.add(category.service_identifier)
    return types
