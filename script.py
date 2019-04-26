import sys

from app import db
from app.models import Category
from app.constants import Service


def add_google_categories():
    category = Category(
        text='food',
        service=Service.GOOGLE,
        service_identifier='restaurant'
    )
    db.session.add(category)

    category = Category(
        text='restaurant',
        service=Service.GOOGLE,
        service_identifier='restaurant'
    )
    db.session.add(category)

    category = Category(
        text='bar',
        service=Service.GOOGLE,
        service_identifier='bar'
    )
    db.session.add(category)

    category = Category(
        text='drinks',
        service=Service.GOOGLE,
        service_identifier='bar'
    )
    db.session.add(category)

    category = Category(
        text='coffee',
        service=Service.GOOGLE,
        service_identifier='coffee'
    )
    db.session.add(category)

    db.session.commit()


def add_foursquare_categories():
    category = Category(
        text='food',
        service=Service.FOURSQUARE,
        service_identifier='food'
    )
    db.session.add(category)

    category = Category(
        text='restaurant',
        service=Service.FOURSQUARE,
        service_identifier='food'
    )
    db.session.add(category)

    category = Category(
        text='bar',
        service=Service.FOURSQUARE,
        service_identifier='drinks'
    )
    db.session.add(category)

    category = Category(
        text='drinks',
        service=Service.FOURSQUARE,
        service_identifier='drinks'
    )
    db.session.add(category)

    category = Category(
        text='coffee',
        service=Service.FOURSQUARE,
        service_identifier='coffee'
    )
    db.session.add(category)

    db.session.commit()


def add_facebook_categories():
    category = Category(
        text='food',
        service=Service.FACEBOOK,
        service_identifier='FOOD_BEVERAGE'
    )
    db.session.add(category)

    category = Category(
        text='restaurant',
        service=Service.FACEBOOK,
        service_identifier='FOOD_BEVERAGE'
    )
    db.session.add(category)

    category = Category(
        text='bar',
        service=Service.FACEBOOK,
        service_identifier='FOOD_BEVERAGE'
    )
    db.session.add(category)

    category = Category(
        text='drinks',
        service=Service.FACEBOOK,
        service_identifier='FOOD_BEVERAGE'
    )
    db.session.add(category)

    category = Category(
        text='coffee',
        service=Service.FACEBOOK,
        service_identifier='FOOD_BEVERAGE'
    )
    db.session.add(category)

    db.session.commit()


def add_service_categories():
    add_foursquare_categories()
    add_google_categories()
    add_facebook_categories()


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
