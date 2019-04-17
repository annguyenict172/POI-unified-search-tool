import json
import sys

from app.helper import snake_case_to_lower_words
from app import db
from app.models import Category
from app.enum import Service


def add_google_categories():
    f = open('files/google_category.txt', 'r')
    for line in f.readlines():
        category_name = line.strip()
        category = Category(
            raw_text=category_name,
            formatted_text=snake_case_to_lower_words(category_name),
            service=Service.GOOGLE,
            service_identifier=category_name
        )
        db.session.add(category)
        db.session.commit()


def add_foursquare_categories():
    f = open('files/foursquare_category.json')
    data = json.load(f)['response']
    for main_category in data['categories']:
        category = Category(
            raw_text=main_category['name'],
            formatted_text=main_category['name'].lower(),
            service=Service.FOURSQUARE,
            service_identifier=main_category['id']
        )
        db.session.add(category)
        db.session.commit()
        for child_category in main_category['categories']:
            category = Category(
                raw_text=child_category['name'],
                formatted_text=child_category['name'].lower(),
                service='Foursquare',
                service_identifier=child_category['id']
            )
            db.session.add(category)
            db.session.commit()


def add_service_categories():
    add_google_categories()
    add_foursquare_categories()


scripts = {
    'add_service_categories': add_service_categories
}


if __name__ == '__main__':
    num_of_arguments = len(sys.argv)
    if num_of_arguments < 2:
        print('Please specify a script. Available scripts are:')
        print(', '.join(scripts.keys()))
    else:
        script = sys.argv[1]
        scripts[script]()
        print('Run {} script successfully!'.format(script))
