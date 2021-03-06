import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l
from flask import request
from elasticsearch import Elasticsearch


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)

    db.init_app(application)
    migrate.init_app(application)
    login.init_app(application)
    mail.init_app(application)
    bootstrap.init_app(application)
    moment.init_app(application)
    babel.init_app(application)
    application.elasticsearch = Elasticsearch([application.config['ELASTICSEARCH_URL']]) \
        if application.config['ELASTICSEARCH_URL'] else None

    from app.errors import bp as errors_bp
    application.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    application.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    application.register_blueprint(main_bp)

    if not application.debug and not application.testing:
        if application.config['MAIL_SERVER']:
            auth = None
            if application.config['MAIL_USERNAME'] or application.config['MAIL_PASSWORD']:
                auth = (application.config['MAIL_USERNAME'],
                        application.config['MAIL_PASSWORD'])
            secure = None
            if application.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(application.config['MAIL_SERVER'],
                          application.config['MAIL_PORT']),
                fromaddr='no-reply@' + application.config['MAIL_SERVER'],
                toaddrs=application.config['ADMINS'], subject='BLOG APP FAILURE!',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            application.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
      '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    application.logger.addHandler(file_handler)

    application.logger.setLevel(logging.INFO)
    application.logger.info('Microblog startup')

    return application

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

from app import models