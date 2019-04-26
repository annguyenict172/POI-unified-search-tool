from app.api import GooglePlaceAPI
from app.models import Category
from app.constants import Service
from app.utils.text_analyzer import extract_nouns_and_location


def extract_arguments(query_text):
    nouns, location = extract_nouns_and_location(query_text)
    geometry = {}
    types = {}
    if location:
        res = GooglePlaceAPI().get_geocoding(location)
        geometry = res.json()['results'][0]['geometry']['location']
    if nouns:
        for service in Service.get_list():
            types[service] = _find_matched_categories(nouns, service)
    return {
        'location': location,
        'types': types,
        'geometry': geometry
    }


def _find_matched_categories(terms, service):
    types = []
    for term in terms:
        categories = Category.query.filter(
            Category.service == service,
            Category.formatted_text.like('%{}%'.format(term))
        ).all()
        for category in categories:
            types.append(category.service_identifier)
    return types
