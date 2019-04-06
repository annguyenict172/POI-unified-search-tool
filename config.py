import os

from dotenv import load_dotenv

base_dir = os.getcwd()
dotenv_path = base_dir + '/.env'
load_dotenv(dotenv_path=dotenv_path)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
