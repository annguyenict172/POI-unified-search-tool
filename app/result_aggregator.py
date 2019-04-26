import uuid

from app.constants import Service
from app.utils.math import get_euclidean_distance
from app.utils.string import get_similar_ratio


class ResultAggregator:
    def __init__(self, responses):
        self.responses = responses

    def aggregate_responses(self):
        results = []

        # Add response from different services to a single list
        for service in Service.get_list():
            items = self.responses[service]

            # Remove duplicate items in a service's response
            appears = {}
            for item in items:
                if appears.get(item['name']) is None:
                    appears[item['name']] = True
                else:
                    items.remove(item)

            results.extend(items)

        # Sort the items by name
        results.sort(key=lambda x: x['name'])

        # Map phase
        distinct_counts = {}
        for i, item in enumerate(results):
            if i == 0:
                item['distinct_id'] = str(uuid.uuid4())
                continue
            else:
                previous_item = results[i-1]
                distance = get_euclidean_distance(results[i-1], item)
                name_similarity = get_similar_ratio(results[i-1]['name'], item['name'])
                if distance < 100 and name_similarity > 70 and item['service'] != previous_item['service']:
                    item['distinct_id'] = previous_item['distinct_id']
                    distinct_counts[item['distinct_id']] += 1
                else:
                    item['distinct_id'] = str(uuid.uuid4())
                    distinct_counts[item['distinct_id']] = 1

        # Reduce phase
        merged_results = []
        for key, value in distinct_counts.items():
            if value > 1:
                similar_items = [item for item in results if item['distinct_id'] == key]
                merged_item = {}
                for item in similar_items:
                    merged_item[item['service']] = item
                merged_results.append(merged_item)
        return merged_results
