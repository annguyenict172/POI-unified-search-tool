import uuid

from app.utils.math import get_euclidean_distance
from app.utils.string import get_similar_ratio

S_MAX = 100
N_MIN = 70


class ResultAggregator:
    def __init__(self, data):
        self.data = data

    def aggregate_results(self):
        # Sort the items by name
        self.data.sort(key=lambda x: x['name'])

        # Map phase
        distinct_counts = {}
        for i, item in enumerate(self.data):
            if i == 0:
                item['distinct_id'] = str(uuid.uuid4())
                distinct_counts[item['distinct_id']] = 1
                continue
            else:
                previous_item = self.data[i-1]
                distance = get_euclidean_distance(self.data[i-1], item)
                name_similarity = get_similar_ratio(self.data[i-1]['name'], item['name'])
                if distance < S_MAX and name_similarity > N_MIN and item['provider'] != previous_item['provider']:
                    item['distinct_id'] = previous_item['distinct_id']
                    distinct_counts[item['distinct_id']] += 1
                else:
                    item['distinct_id'] = str(uuid.uuid4())
                    distinct_counts[item['distinct_id']] = 1

        # Reduce phase
        results = []
        for key, value in distinct_counts.items():
            similar_items = [item for item in self.data if item['distinct_id'] == key]
            merged_item = {}
            for item in similar_items:
                merged_item[item['provider']] = item
            results.append(merged_item)

        return results
