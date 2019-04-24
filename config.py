import os

from dotenv import load_dotenv

base_dir = os.getcwd()
dotenv_path = base_dir + '/.env'
load_dotenv(dotenv_path=dotenv_path)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    GOOGLE_PLACE_API_KEY = os.environ.get('GOOGLE_PLACE_API_KEY')
    FOURSQUARE_CLIENT_ID = os.environ.get('FOURSQUARE_CLIENT_ID')
    FOURSQUARE_CLIENT_SECRET = os.environ.get('FOURSQUARE_CLIENT_SECRET')
    FOURSQUARE_OAUTH_TOKEN = os.environ.get('FOURSQUARE_OAUTH_TOKEN')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/app.db'.format(base_dir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
