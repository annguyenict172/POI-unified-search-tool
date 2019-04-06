import os
import json


def load_categories():
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, 'data.json')
    file_ = open(file_path, 'r')
    content = file_.read()
    return json.loads(content)
