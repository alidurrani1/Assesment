import os

from celery.schedules import crontab


class Config(object):
    """
    Basic Configurations of App with Database
    """
    TESTING = False
    DEBUG = False
    MYSQL_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD', 'a1s2d3f4')
    MYSQL_HOST = os.environ.get('MYSQL_ROOT_HOST', 'db')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'flask_app')
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'
    SECRET_KEY = 'ANY_SECRET_KEY'
    SESSION_COOKIE_SECURE = True


class EmailConfigurations(Config):
    """
    Email Configurations for App
    """
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'any_mail@gmail.com'
    MAIL_PASSWORD = 'any_paswd'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SESSION_COOKIE_SECURE = True


class CeleryConfigurations(Config):
    """

    Celery Configurations for app

    """

    CELERY_CONFIG = {
        'broker_url': 'redis://redis:6379/0',
        'result_backend': 'redis://redis:6379/0',
    }
    CELERYBEAT_SCHEDULE = {
        'say-every-5-seconds': {
            'task': 'store',
            "schedule": crontab(hour='*/24'),
            # "schedule": 5.00,
        }
    }
