from app.constants import Provider
from app.schemas import GoogleSchema, FacebookSchema, FoursquareSchema

Schema = {
    Provider.GOOGLE: GoogleSchema,
    Provider.FOURSQUARE: FoursquareSchema,
    Provider.FACEBOOK: FacebookSchema
}


class ResponseFormatter:
    def __init__(self, raw_responses):
        self.raw_responses = raw_responses

    def format_responses(self):
        results = []

        # Add response from different providers to a single list
        for provider in Provider.get_list():
            # Use Schema as an Adapter to format response to a consistent format
            items = Schema[provider]().dump(self.raw_responses[provider], many=True).data

            # Remove duplicate items in a provider's response
            appears = {}
            for item in items:
                try:
                    if appears.get(item['id']) is None:
                        appears[item['id']] = True
                    else:
                        items.remove(item)
                except KeyError:
                    items.remove(item)

            results.extend(items)

        return results
