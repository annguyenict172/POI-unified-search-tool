import nltk

from app.api import GooglePlaceAPI
from app.models import Category
from app.constants import Service


def extract_arguments(query_text):
    location, name, nouns = _extract_potential_keywords(query_text)
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
        'name': name,
        'types': types,
        'geometry': geometry
    }


def _extract_potential_keywords(text):
    nouns = []
    name = ''
    location = ''

    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    for w in tagged:
        if w[1] == 'NN':
            nouns.append(w[0])

    for chunk in nltk.ne_chunk(tagged):
        if hasattr(chunk, 'label'):
            if chunk.label() == 'PERSON':
                name = ' '.join(c[0] for c in chunk)
            if chunk.label() == 'GPE':
                location = ' '.join(c[0] for c in chunk)

    return location, name, nouns


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
