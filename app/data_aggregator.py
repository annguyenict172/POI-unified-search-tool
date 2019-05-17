import uuid

from app.utils.math import get_euclidean_distance
from app.utils.string import get_similar_ratio


class DataAggregator:
    def __init__(self, data):
        self.data = data

    def aggregate_data(self):
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
                if distance < 100 and name_similarity > 70 and item['service'] != previous_item['service']:
                    item['distinct_id'] = previous_item['distinct_id']
                    distinct_counts[item['distinct_id']] += 1
                else:
                    item['distinct_id'] = str(uuid.uuid4())
                    distinct_counts[item['distinct_id']] = 1

        # Reduce phase
        results = []
        for key, value in distinct_counts.items():
            if value >= 3:
                similar_items = [item for item in self.data if item['distinct_id'] == key]
                merged_item = {}
                for item in similar_items:
                    merged_item[item['service']] = item
                results.append(merged_item)
        print(len(results))
        return results
