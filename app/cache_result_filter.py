from .models import Category
from .utils.math import get_euclidean_distance
from .constants import Service


class CacheResultFilter:
    @staticmethod
    def filter_cache_results(args, cache_results):
        current_location = {
            'lat': float(args.get('location').split(',')[0]),
            'lng': float(args.get('location').split(',')[1])
        }
        appeared = {
            Service.FACEBOOK: {},
            Service.FOURSQUARE: {},
            Service.GOOGLE: {}
        }
        if args.get('categories'):
            results = []
            categories = args.get('categories').split(',')
            counts = {}
            for category in categories:
                counts[category] = 0
            for category in categories:
                gg_cat = Category.query.filter_by(service='google', text=category).first().service_identifier
                fb_cat = Category.query.filter_by(service='facebook', text=category).first().service_identifier
                fs_cat = Category.query.filter_by(service='foursquare', text=category).first().service_identifier
                fb_cat = '["{}"]'.format(fb_cat)
                for item in cache_results:
                    if item.get('facebook') \
                            and item['facebook'].get('unified_type') == fb_cat\
                            and get_euclidean_distance(current_location, item['facebook']) <= args['radius']\
                            and appeared['facebook'].get(item['facebook']['name']) is None:
                        counts[category] += 1
                        results.append(item)
                        appeared['facebook'][item['facebook']['name']] = True
                        if item.get('google'):
                            appeared['google'][item['google']['name']] = True
                        if item.get('foursquare'):
                            appeared['foursquare'][item['foursquare']['name']] = True
                        continue
                    elif item.get('google') \
                            and item['google'].get('unified_type') == gg_cat\
                            and get_euclidean_distance(current_location, item['google']) <= args['radius']\
                            and appeared['google'].get(item['google']['name']) is None:
                        counts[category] += 1
                        results.append(item)
                        appeared['google'][item['google']['name']] = True
                        if item.get('facebook'):
                            appeared['facebook'][item['facebook']['name']] = True
                        if item.get('foursquare'):
                            appeared['foursquare'][item['foursquare']['name']] = True
                        continue
                    elif item.get('foursquare') \
                            and item['foursquare'].get('unified_type') == fs_cat\
                            and get_euclidean_distance(current_location, item['foursquare']) <= args['radius']\
                            and appeared['foursquare'].get(item['foursquare']['name']) is None:
                        counts[category] += 1
                        results.append(item)
                        appeared['foursquare'][item['foursquare']['name']] = True
                        if item.get('google'):
                            appeared['google'][item['google']['name']] = True
                        if item.get('facebook'):
                            appeared['facebook'][item['facebook']['name']] = True
                        continue
            remaining_categories = []
            for category in categories:
                if counts[category] == 0:
                    remaining_categories.append(category)
            return results, remaining_categories
        elif args.get('keyword'):
            results = []
            for item in cache_results:
                if item.get('facebook') \
                        and args.get('keyword').lower() in item['facebook']['name'].lower() \
                        and get_euclidean_distance(current_location, item['facebook']) <= args['radius']\
                        and appeared['facebook'].get(item['facebook']['name']) is None:
                    appeared['facebook'][item['facebook']['name']] = True
                    if item.get('google'):
                        appeared['google'][item['google']['name']] = True
                    if item.get('foursquare'):
                        appeared['foursquare'][item['foursquare']['name']] = True
                    results.append(item)
                    continue
                elif item.get('google') \
                        and args.get('keyword').lower() in item['google']['name'].lower() \
                        and get_euclidean_distance(current_location, item['google']) <= args['radius']\
                        and appeared['google'].get(item['google']['name']) is None:
                    results.append(item)
                    appeared['google'][item['google']['name']] = True
                    if item.get('facebook'):
                        appeared['facebook'][item['facebook']['name']] = True
                    if item.get('foursquare'):
                        appeared['foursquare'][item['foursquare']['name']] = True
                    continue
                elif item.get('foursquare') \
                        and args.get('keyword').lower() in item['foursquare']['name'].lower() \
                        and get_euclidean_distance(current_location, item['foursquare']) <= args['radius']\
                        and appeared['foursquare'].get(item['foursquare']['name']) is None:
                    results.append(item)
                    appeared['foursquare'][item['foursquare']['name']] = True
                    if item.get('google'):
                        appeared['google'][item['google']['name']] = True
                    if item.get('facebook'):
                        appeared['facebook'][item['facebook']['name']] = True
                    continue
            return results, []
        else:
            results = []
            for item in cache_results:
                if item.get('facebook') \
                        and get_euclidean_distance(current_location, item['facebook']) <= args['radius']\
                        and appeared['facebook'].get(item['facebook']['name']) is None:
                    appeared['facebook'][item['facebook']['name']] = True
                    if item.get('google'):
                        appeared['google'][item['google']['name']] = True
                    if item.get('foursquare'):
                        appeared['foursquare'][item['foursquare']['name']] = True
                    results.append(item)
                    continue
                elif item.get('google') \
                        and get_euclidean_distance(current_location, item['google']) <= args['radius']\
                        and appeared['google'].get(item['google']['name']) is None:
                    results.append(item)
                    appeared['google'][item['google']['name']] = True
                    if item.get('facebook'):
                        appeared['facebook'][item['facebook']['name']] = True
                    if item.get('foursquare'):
                        appeared['foursquare'][item['foursquare']['name']] = True
                    continue
                elif item.get('foursquare') \
                        and get_euclidean_distance(current_location, item['foursquare']) <= args['radius']\
                        and appeared['foursquare'].get(item['foursquare']['name']) is None:
                    results.append(item)
                    appeared['foursquare'][item['foursquare']['name']] = True
                    if item.get('google'):
                        appeared['google'][item['google']['name']] = True
                    if item.get('facebook'):
                        appeared['facebook'][item['facebook']['name']] = True
                    continue
            return results, []
