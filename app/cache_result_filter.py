from .models import Category

class CacheResultFilter:
    @staticmethod
    def filter_cache_results(args, cache_results):
        results = []
        categories = args.get('categories').split(',') if args.get('categories') else []
        counts = {}
        for category in categories:
            counts[category] = 0
        for category in categories:
            gg_cat = Category.query.filter_by(service='google', text=category).first().service_identifier
            fb_cat = Category.query.filter_by(service='facebook', text=category).first().service_identifier
            fs_cat = Category.query.filter_by(service='foursquare', text=category).first().service_identifier
            for item in cache_results:
                if item.get('facebook') and item['facebook']['unified_type'] == fb_cat:
                    counts[category] += 1
                    results.append(item)
                elif item.get('google') and item['google']['unified_type'] == gg_cat:
                    counts[category] += 1
                    results.append(item)
                elif item.get('foursquare') and item['foursquare']['unified_type'] == fs_cat:
                    counts[category] += 1
                    results.append(item)
        remaining_categories = []
        for category in categories:
            if counts[category] == 0:
                remaining_categories.append(category)

        return results, remaining_categories
