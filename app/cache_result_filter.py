from copy import deepcopy

from .models import Term
from .utils.math import get_euclidean_distance
from .constants import Provider


class CacheResultFilter:
    @staticmethod
    def filter_cache_results(args, cache_results):
        # Convert the location parameter from string to float
        current_location = {
            'lat': float(args.get('location').split(',')[0]),
            'lng': float(args.get('location').split(',')[1])
        }
        categories = keyword = None
        if args.get('categories'):
            categories = args.get('categories').split(',')
            provider_categories = {}
            for provider in Provider.get_list():
                provider_categories[provider] = [
                    term_model.matched_term for term_model in Term.query.filter(
                        Term.provider == provider,
                        Term.term.in_(categories)
                    )
                ]
            remaining_categories = deepcopy(provider_categories)
        if args.get('keyword'):
            keyword = args.get('keyword')
        radius = args.get('radius')

        results = []
        appeared = {}
        for item in cache_results:
            if item['provider'] not in Provider.get_list():
                continue
            if appeared.get(item['name']) is not None:
                continue
            if categories and not item.get('unified_category'):
                continue
            if categories and item['unified_category'] not in provider_categories[item['provider']]:
                continue
            if keyword and keyword.lower() not in item['name'].lower():
                continue
            if get_euclidean_distance(current_location, item) > radius:
                continue

            results.append(item)
            if categories and item.get('unified_category') \
                and item.get('unified_category') in remaining_categories[item.get('provider')]:
                    for category in remaining_categories[item.get('provider')]:
                        if category == item.get('unified_category'):
                            remaining_categories[item.get('provider')].remove(category)
            appeared[item['id']] = True

        unified_remaining_categories = []
        for category in remaining_categories[Provider.GOOGLE]:
            term_model = Term.query.filter_by(provider=Provider.GOOGLE, matched_term=category).first()
            unified_remaining_categories.append(term_model.term)

        return results, unified_remaining_categories
