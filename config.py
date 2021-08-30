import os
basedirectory = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'good-at-guessing'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedirectory, 'application.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
