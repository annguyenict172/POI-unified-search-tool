from app.constants import Service
from app.schemas import GoogleSchema, FacebookSchema, FoursquareSchema

Schema = {
    Service.GOOGLE: GoogleSchema,
    Service.FOURSQUARE: FoursquareSchema,
    Service.FACEBOOK: FacebookSchema
}


class DataPreprocessor:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        results = []

        # Add response from different services to a single list
        for service in Service.get_list():
            # Use Schema as an Adapter
            items = Schema[service]().dump(self.data[service], many=True).data

            # Remove duplicate items in a service's response
            appears = {}
            for item in items:
                if appears.get(item['name']) is None:
                    appears[item['name']] = True
                else:
                    items.remove(item)

            results.extend(items)

        return results
